from time import time
import concurrent.futures as cf
import numpy as np
from worms import Vertex, Edge, precompute_splicedb
from worms.bblock import bblock_dump_pdb, _BBlock
from worms.vertex import _Vertex
from worms.edge import _Edge
import worms

from worms.util import InProcessExecutor
from pprint import pprint
from logging import info
import string


def _validate_bbs_verts(bbs, verts):
    assert len(bbs) == len(verts)
    for bb, vert in zip(bbs, verts):
        if vert is None: continue
        assert 0 <= np.min(vert.ibblock)
        assert np.max(vert.ibblock) < len(bb)


class SearchSpaceDag:
    def __init__(self, bbspec, bbs, verts, edges):
        _validate_bbs_verts(bbs, verts)
        assert isinstance(bbs[0][0], _BBlock)
        assert isinstance(verts[0], (_Vertex, type(None)))
        assert len(edges) == 0 or isinstance(edges[0], _Edge)
        if bbspec:
            assert len(bbspec) == len(bbs)
        assert len(edges) == 0 or len(edges) + 1 == len(verts)
        self.bbspec = bbspec
        self.bbs = tuple(bbs)
        self.verts = tuple(verts)
        self.edges = tuple(edges)

    def __getstate__(self):
        return (
            self.bbspec,
            [[x._state for x in bb] for bb in self.bbs],
            [x._state for x in self.verts],
            [x._state for x in self.edges]
        )

    def __setstate__(self, state):
        self.bbspec = state[0]
        self.bbs = tuple(tuple(_BBlock(*x) for x in bb) for bb in state[1])
        self.verts = tuple(_Vertex(*x) for x in state[2])
        self.edges = tuple(_Edge(*x) for x in state[3])
        _validate_bbs_verts(self.bbs, self.verts)
        assert len(self.bbs) == len(self.verts) == len(self.edges) + 1


def simple_search_dag(
        criteria,
        db=None,
        nbblocks=100,
        shuf=False,
        min_seg_len=15,
        parallel=False,
        verbosity=0,
        timing=0,
        modbbs=None,
        make_edges=True,
        merge_bblock=None,
        precache_splices=False,
        precache_only=False,
        bbs=None,
        only_seg=None,
        **kw
):
    bbdb, spdb = db
    queries, directions = zip(*criteria.bbspec)
    tdb = time()
    if bbs is None:
        info('bblock queries: ' + str(queries))
        info('directions: ' + str(directions))
        bbmap = {
            q: bbdb.query(q, max_bblocks=nbblocks, shuffle=shuf)
            for q in set(queries)
        }
        for k, v in bbmap.items():
            assert len(v) > 0, 'no bblocks for query: "' + k + '"'
        bbs = [bbmap[q] for q in queries]
    else:
        bbs = bbs.copy()
    assert len(bbs) == len(criteria.bbspec)

    if modbbs: modbbs(bbs)
    if merge_bblock is not None and merge_bblock >= 0:
        # print('which_mergebb', criteria.bbspec, criteria.which_mergebb())
        for i in criteria.which_mergebb():
            bbs[i] = (bbs[i][merge_bblock], )

    tdb = time() - tdb
    info(
        f'bblock creation time {tdb:7.3f} num bbs: ' +
        str([len(x) for x in bbs])
    )

    if precache_splices:
        bbnames = [[bytes(bb.file) for bb in bbtup] for bbtup in bbs]
        bbpairs = set()
        for bb1, bb2, dirn1 in zip(bbnames, bbnames[1:], directions):
            rev = dirn1[1] == 'N'
            bbpairs.update((b, a) if rev else (a, b) for a in bb1 for b in bb2)
        precompute_splicedb(
            db, bbpairs, verbosity=verbosity, parallel=parallel, **kw
        )
    if precache_only:
        return bbs

    tvertex = time()
    exe = InProcessExecutor()

    if parallel:
        exe = cf.ThreadPoolExecutor(max_workers=parallel)
    with exe as pool:
        if only_seg is not None:
            save = bbs, directions
            bbs = [bbs[only_seg]]
            directions = [directions[only_seg]]
        futures = list()
        for bb, dirn in zip(bbs, directions):
            futures.append(
                pool.submit(Vertex, bb, dirn, min_seg_len=min_seg_len)
            )
        verts = [f.result() for f in futures]
        if only_seg is not None:
            verts = ([None] * only_seg + verts +
                     [None] * (len(queries) - only_seg - 1))
            bbs, directions = save
    tvertex = time() - tvertex
    info(
        f'vertex creation time {tvertex:7.3f} num verts ' +
        str([v.len if v else 0 for v in verts])
    )

    edges = []
    if make_edges:
        tedge = time()
        edges = [
            Edge(
                verts[i],
                bbs[i],
                verts[i + 1],
                bbs[i + 1],
                splicedb=spdb,
                verbosity=verbosity,
                precache_splices=precache_splices,
                **kw
            ) for i in range(len(verts) - 1)
        ]
        tedge = time() - tedge
        # if verbosity > 1:
        # print_edge_summary(edges)
        info(
            f'edge creation time {tedge:7.3f} num splices ' +
            str([e.total_allowed_splices()
                 for e in edges]) + ' num exits ' + str([e.len for e in edges])
        )
        spdb.sync_to_disk()

    toret = SearchSpaceDag(criteria.bbspec, bbs, verts, edges)
    if timing:
        toret = toret, tdb, tvertex, tedge
    return toret


def print_edge_summary(edges):
    print('  splice stats: ', end='')
    for e in edges:
        nsplices = e.total_allowed_splices()
        ntot = e.nout * e.nent
        print(f'({nsplices:,} {nsplices*100.0/ntot:5.2f}%)', end=' ')
    print()


def graph_dump_pdb(out, ssdag, idx, pos, join='splice', trim=True):
    close = False
    if isinstance(out, str):
        out = open(out, 'w')
        close = True
    assert len(idx) == len(pos)
    assert idx.ndim == 1
    assert pos.ndim == 3
    assert pos.shape[-2:] == (4, 4)
    chain, anum, rnum = 0, 1, 1
    for i, tup in enumerate(zip(ssdag.bbs, ssdag.verts, idx, pos)):
        bbs, vert, ivert, x = tup
        chain, anum, rnum = bblock_dump_pdb(
            out=out,
            bblock=bbs[vert.ibblock[ivert]],
            dirn=vert.dirn if trim else (2, 2),
            splice=vert.ires[ivert] if trim else (-1, -1),
            pos=x,
            chain=chain,
            anum=anum,
            rnum=rnum,
            join=join,
        )
    if close: out.close()