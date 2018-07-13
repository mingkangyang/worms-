import string
import numpy as np
import numba as nb
from worms import util
from worms.util import jit
from worms.vis import format_atom
from worms.filters.clash import _chain_bounds
import numba.types as nt
import homog


def BBlock(entry, pdbfile, filehash, pose, ss):

    chains = util.get_chain_bounds(pose)
    ss = np.frombuffer(ss.encode(), dtype='i1')
    ncac = util.get_bb_coords(pose)
    stubs = _ncac_to_stubs(ncac)

    assert len(pose) == len(ncac)
    assert len(pose) == len(stubs)
    assert len(pose) == len(ss)
    conn = _make_connections_array(entry['connections'], chains)
    if len(conn) is 0:
        print('bad conn info!', pdbfile)
        return None, pdbfile  # new, missing
    if ncac.shape[-1] is 4:
        ncac = ncac.astype(np.float64)
    elif ncac.shape[-1] is 3:
        tmp = np.ones((ncac.shape[0], 3, 4), dtype=np.float64)
        tmp[..., :3] = ncac
        ncac = tmp
    else:
        assert 0, 'bad ncac'

    npfb = np.frombuffer
    bblock = _BBlock(
        connections=conn,
        file=npfb(entry['file'].encode(), dtype='i1'),
        filehash=filehash,
        components=npfb(str(entry['components']).encode(), dtype='i1'),
        protocol=npfb(entry['protocol'].encode(), dtype='i1'),
        name=npfb(entry['name'].encode(), dtype='i1'),
        classes=npfb(','.join(entry['class']).encode(), 'i1'),
        validated=entry['validated'],
        _type=npfb(entry['type'].encode(), dtype='i1'),
        base=npfb(entry['base'].encode(), dtype='i1'),
        ncac=np.ascontiguousarray(ncac),
        chains=np.array(chains, dtype='i4'),
        ss=ss,
        stubs=np.ascontiguousarray(stubs.astype('f8')),
    )

    return bblock


def bblock_dump_pdb(
        out,
        bblock,
        dirn=(2, 2),
        splice=(-1, -1),
        join='splice',
        pos=np.eye(4),
        chain=0,
        anum=1,
        rnum=1
):
    close = False
    if isinstance(out, str):
        out = open(out, 'w')
        close = True

    chains0 = _chain_bounds(dirn, splice, bblock.chains, trim=0)
    if dirn[0] == 2 and dirn[1] == 2:
        chains = chains0
    else:
        sponly = _chain_bounds(
            dirn, splice, bblock.chains, trim=0, spliced_only=1
        )
        # chains will have insplice at first ops, outsplice at last pos
        # either could be none
        chains = list()
        chains.append(sponly[0] if dirn[0] < 2 else None)
        for c in chains0:
            if np.all(sponly[0] == c) or np.all(sponly[-1] == c):
                continue
            chains.append(c)
        chains.append(sponly[-1] if dirn[1] < 2 else None)

    aname = [' N  ', ' CA ', ' C  ']
    for ic, lbub in enumerate(chains):
        if lbub is None: continue
        for i in range(*lbub):
            for j in (0, 1, 2):
                xyz = pos @ bblock.ncac[i, j]
                out.write(
                    format_atom(
                        atomi=anum,
                        atomn=aname[j],
                        resn='GLY',
                        chain=string.ascii_uppercase[chain],
                        resi=rnum,
                        x=xyz[0],
                        y=xyz[1],
                        z=xyz[2],
                        occ=1.0,
                    )
                )
                anum += 1
            rnum += 1
        if join == 'bb': continue
        if join == 'splice' and ic + 1 == len(chains) and dirn[1] < 2:
            continue
        chain += 1
    if join == 'bb': chain += 1
    if close: out.close()
    return chain, anum, rnum


def _ncac_to_stubs(ncac):
    """
        Vector const & center,
        Vector const & a,
        Vector const & b,
        Vector const & c
    )
    {
        Vector e1( a - b);
        e1.normalize();

        Vector e3( cross( e1, c - b ) );
        e3.normalize();

        Vector e2( cross( e3,e1) );
        M.col_x( e1 ).col_y( e2 ).col_z( e3 );
        v = center;
    """
    assert ncac.shape[1:] == (3, 4)
    stubs = np.zeros((len(ncac), 4, 4), dtype=np.float64)
    ca2n = (ncac[:, 0] - ncac[:, 1])[..., :3]
    ca2c = (ncac[:, 2] - ncac[:, 1])[..., :3]
    # tgt1 = ca2n + ca2c  # thought this might make
    # tgt2 = ca2n - ca2c  # n/c coords match better
    tgt1 = ca2n  # rosetta style
    tgt2 = ca2c  # seems better
    a = tgt1
    a /= np.linalg.norm(a, axis=-1)[:, None]
    c = np.cross(a, tgt2)
    c /= np.linalg.norm(c, axis=-1)[:, None]
    b = np.cross(c, a)
    assert np.allclose(np.sum(a * b, axis=-1), 0)
    assert np.allclose(np.sum(b * c, axis=-1), 0)
    assert np.allclose(np.sum(c * a, axis=-1), 0)
    assert np.allclose(np.linalg.norm(a, axis=-1), 1)
    assert np.allclose(np.linalg.norm(b, axis=-1), 1)
    assert np.allclose(np.linalg.norm(c, axis=-1), 1)
    stubs[:, :3, 0] = a
    stubs[:, :3, 1] = b
    stubs[:, :3, 2] = c
    stubs[:, :3, 3] = ncac[:, 1, :3]
    stubs[:, 3, 3] = 1
    return stubs


@nb.jitclass((
    ('connections', nt.int32[:, :]),
    ('file'       , nt.int8[:]),
    ('filehash'   , nt.int64),
    ('components' , nt.int8[:]),
    ('protocol'   , nt.int8[:]),
    ('name'       , nt.int8[:]),
    ('classes'    , nt.int8[:]),
    ('validated'  , nt.boolean),
    ('_type'      , nt.int8[:]),
    ('base'       , nt.int8[:]),
    ('ncac'       , nt.float64[:, :, :]),
    ('chains'     , nt.int32[:,:]),
    ('ss'         , nt.int8[:]),
    ('stubs'      , nt.float64[:, :, :]),
))  # yapf: disable
class _BBlock:
    def __init__(
            self, connections, file, filehash, components, protocol, name,
            classes, validated, _type, base, ncac, chains, ss, stubs
    ):
        self.connections = connections
        self.file = file
        self.filehash = filehash
        self.components = components
        self.protocol = protocol
        self.name = name
        self.classes = classes
        self.validated = validated
        self._type = _type
        self.base = base
        self.ncac = ncac
        self.chains = chains
        self.ss = ss
        self.stubs = stubs
        assert np.isnan(np.sum(self.ncac)) == False
        assert np.isnan(np.sum(self.stubs)) == False
        assert np.isnan(np.sum(self.ss)) == False
        assert np.isnan(np.sum(self.chains)) == False

    @property
    def n_connections(self):
        return len(self.connections)

    def conn_dirn(self, i):
        return self.connections[i, 0]

    def conn_resids(self, i):
        return self.connections[i, 2:self.connections[i, 1]]

    @property
    def _state(self):
        """TODO: Summary

        Returns:
            TYPE: Description
        """
        return (
            self.connections, self.file, self.filehash, self.components,
            self.protocol, self.name, self.classes, self.validated, self._type,
            self.base, self.ncac, self.chains, self.ss, self.stubs
        )


@jit
def chain_of_ires(bb, ires):
    """Summary

    Args:
        bb (TYPE): Description
        ires (TYPE): Description

    Returns:
        TYPE: Description
    """
    chain = np.empty_like(ires)
    for i, ir in enumerate(ires):
        if ir < 0:
            chain[i] = -1
        else:
            for c in range(len(bb.chains)):
                if bb.chains[c, 0] <= ir < bb.chains[c, 1]:
                    chain[i] = c
    return chain


def _make_connections_array(entries, chain_bounds):
    """TODO: Summary

    Args:
        entries (TYPE): Description
        chain_bounds (TYPE): Description

    Returns:
        TYPE: Description
    """
    try:
        reslists = [_get_connection_residues(e, chain_bounds) for e in entries]
    except Exception as e:
        print('make_connections_array failed on', entries, 'error was:', e)
        return np.zeros((0, 0))
    reslists = sorted(reslists, key=lambda x: x[0])
    mx = max(len(x) for x in reslists)
    conn = np.zeros((len(reslists), mx + 2), 'i4') - 1
    for i, ires_ary in enumerate(reslists):
        conn[i, 0] = entries[i]['direction'] == 'C'
        conn[i, 1] = len(ires_ary) + 2
        conn[i, 2:conn[i, 1]] = ires_ary
    return conn
    # print(chain_bounds)
    # print(repr(conn))


def _get_connection_residues(entry, chain_bounds):
    """TODO: Summary

    Args:
        entry (TYPE): Description
        chain_bounds (TYPE): Description

    Returns:
        TYPE: Description
    """
    chain_bounds[-1][-1]
    r, c, d = entry['residues'], int(entry['chain']), entry['direction']
    if isinstance(r, str) and r.startswith('['):
        r = eval(r)
    if isinstance(r, list):
        try:
            return [int(_) for _ in r]
        except ValueError:
            assert len(r) is 1
            r = r[0]
    if r.count(','):
        c2, r = r.split(',')
        assert int(c2) == c
    b, e = r.split(':')
    if b == '-': b = 0
    if e == '-': e = -1
    nres = chain_bounds[c - 1][1] - chain_bounds[c - 1][0]
    b = int(b) if b else 0
    e = int(e) if e else nres
    if e < 0: e += nres
    return np.array(range(*chain_bounds[c - 1])[b:e], dtype='i4')


def bblock_components(bblock):
    """TODO: Summary

    Args:
        bblock (TYPE): Description

    Returns:
        TYPE: Description
    """
    return eval(bytes(bblock.components))


def bblock_str(bblock):
    """TODO: Summary

    Args:
        bblock (TYPE): Description

    Returns:
        TYPE: Description
    """
    return '\n'.join([
        'jitclass BBlock(',
        '    file=' + str(bytes(bblock.file)),
        '    components=' + str(bblock_components(bblock)),
        '    protocol=' + str(bytes(bblock.protocol)),
        '    name=' + str(bytes(bblock.name)),
        '    classes=' + str(bytes(bblock.classes)),
        '    validated=' + str(bblock.validated),
        '    _type=' + str(bytes(bblock._type)),
        '    base=' + str(bytes(bblock.base)),
        '    ncac=array(shape=' + str(bblock.ncac.shape) + ', dtype=' +
        str(bblock.ncac.dtype) + ')',
        '    chains=' + str(bblock.chains),
        '    ss=array(shape=' + str(bblock.ss.shape) + ', dtype=' +
        str(bblock.ss.dtype) + ')',
        '    stubs=array(shape=' + str(bblock.stubs.shape) + ', dtype=' +
        str(bblock.connections.dtype) + ')',
        '    connectionsZ=array(shape=' + str(bblock.connections.shape) +
        ', dtype=' + str(bblock.connections.dtype) + ')',
        ')',
    ])
