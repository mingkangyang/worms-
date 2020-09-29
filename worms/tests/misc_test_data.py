import numpy as np

peace_sign_test_segpos = np.array([
   [
      [
         [1.00000000e00, 0.00000000e00, 0.00000000e00, 0.00000000e00],
         [0.00000000e00, 1.00000000e00, 0.00000000e00, 0.00000000e00],
         [0.00000000e00, 0.00000000e00, 1.00000000e00, 0.00000000e00],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [7.25342383e-01, 3.92040358e-01, -5.65846962e-01, -6.69729964e-01],
         [2.55375487e-01, 6.10088124e-01, 7.50050560e-01, -5.98510947e00],
         [6.39266601e-01, -6.88546904e-01, 3.42405276e-01, 1.19550772e01],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [-8.11008343e-01, 5.32960051e-01, 2.41286244e-01, -7.77763579e00],
         [-2.53192363e-01, 5.20580078e-02, -9.66014281e-01, -7.58131200e00],
         [-5.27407902e-01, -8.44537475e-01, 9.27219361e-02, 1.68390177e01],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [9.54598101e-01, 2.97328373e-01, 1.83930723e-02, -4.15447062e00],
         [-2.44511276e-01, 7.46762288e-01, 6.18514608e-01, -9.67171827e00],
         [1.70166689e-01, -5.94930184e-01, 7.85558002e-01, 2.12457643e01],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [9.36541066e-01, 2.17138702e-01, -2.75211947e-01, 1.27541525e00],
         [3.28260253e-01, -2.67683409e-01, 9.05864669e-01, -4.24335546e00],
         [1.23028606e-01, -9.38720606e-01, -3.21974510e-01, 3.27541329e01],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [-9.75302607e-01, 1.99240799e-01, 9.53306315e-02, -3.79519678e00],
         [-2.15661298e-01, -7.65818206e-01, -6.05815715e-01, 9.35791873e-01],
         [-4.76972739e-02, -6.11412773e-01, 7.89873022e-01, 3.76925930e01],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [2.83875827e-01, 7.12669212e-01, -6.41495993e-01, -7.48139851e00],
         [9.35812175e-01, -6.01119917e-02, 3.47335747e-01, 6.49157142e00],
         [2.08973891e-01, -6.98919983e-01, -6.83988867e-01, 4.01021317e01],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [9.15244941e-01, -2.37811009e-01, 3.25227032e-01, -1.07770464e01],
         [-3.08468884e-01, 1.05663792e-01, 9.45347614e-01, 1.71820276e01],
         [-2.59178791e-01, -9.65547040e-01, 2.33509541e-02, 4.82023740e01],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [8.33543911e-01, -8.81568035e-03, 5.52382867e-01, -1.38893437e01],
         [3.53290470e-01, -7.60192265e-01, -5.45246333e-01, 7.68728168e00],
         [4.24723900e-01, 6.49638364e-01, -6.30539138e-01, 6.01638902e01],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [5.40321024e-01, -3.14116629e-01, -7.80630472e-01, -1.83696129e01],
         [1.32374129e-01, -8.84428542e-01, 4.47507815e-01, -9.71724233e-01],
         [-8.30981516e-01, -3.45133159e-01, -4.36294421e-01, 6.54764466e01],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [8.36268936e-01, -5.03278367e-01, 2.17635363e-01, -2.65451236e01],
         [-2.30649238e-01, 3.72111203e-02, 9.72325183e-01, -1.17387907e01],
         [-4.97448686e-01, -8.63322777e-01, -8.49622676e-02, 6.84132195e01],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [-2.36063755e-01, 6.09925431e-01, 7.56481905e-01, -3.42653055e01],
         [-9.69840202e-01, -9.92552651e-02, -2.22617102e-01, -1.02788421e01],
         [-6.06950199e-02, -7.86218392e-01, 6.14960774e-01, 6.52965512e01],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [-3.24859617e-01, -1.26458694e-01, -9.37269667e-01, -3.29481309e01],
         [9.19809869e-01, -2.72811290e-01, -2.81999655e-01, -5.51209590e00],
         [-2.20036439e-01, -9.53720189e-01, 2.04943326e-01, 6.17667181e01],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [-6.68443285e-01, -3.16157037e-01, 6.73222328e-01, -3.17139062e01],
         [9.71007099e-02, -9.34505385e-01, -3.42448737e-01, -1.21224900e01],
         [7.37397469e-01, -1.63537192e-01, 6.55362922e-01, 5.29319102e01],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [-4.21318988e-01, 6.36946398e-01, 6.45592439e-01, -3.10839784e01],
         [4.71259412e-01, -4.54444743e-01, 7.55906437e-01, -1.77754176e01],
         [7.74857973e-01, 6.22719248e-01, -1.08700785e-01, 4.61171812e01],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [-6.27675862e-01, 5.87313103e-01, -5.10966076e-01, -2.03562620e01],
         [-6.54261355e-02, 6.14247413e-01, 7.86396552e-01, -2.64993944e01],
         [7.75720590e-01, 5.27032669e-01, -3.47122648e-01, 4.65662460e01],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [-1.92486843e-01, 3.73602498e-02, -9.80588103e-01, -9.70032738e00],
         [9.46683712e-01, -2.56000822e-01, -1.95585092e-01, -1.86571993e01],
         [-2.58338469e-01, -9.65954342e-01, 1.39084502e-02, 4.85964069e01],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
   ],
   [
      [
         [1.00000000e00, 0.00000000e00, 0.00000000e00, 0.00000000e00],
         [0.00000000e00, 1.00000000e00, 0.00000000e00, 0.00000000e00],
         [0.00000000e00, 0.00000000e00, 1.00000000e00, 0.00000000e00],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [7.25342383e-01, 3.92040358e-01, -5.65846962e-01, -6.69729964e-01],
         [2.55375487e-01, 6.10088124e-01, 7.50050560e-01, -5.98510947e00],
         [6.39266601e-01, -6.88546904e-01, 3.42405276e-01, 1.19550772e01],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [1.89307580e-01, 7.62848250e-01, -6.18243631e-01, -4.73271557e00],
         [8.61740795e-01, -4.30900723e-01, -2.67819659e-01, 1.39073390e00],
         [-4.70707386e-01, -4.82065466e-01, -7.38950231e-01, 1.26867618e01],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [4.81875316e-01, 8.75117726e-01, -4.43299623e-02, -8.00869493e00],
         [-4.50763621e-01, 2.04189905e-01, -8.68975627e-01, -2.32264512e00],
         [-7.51404244e-01, 4.38720239e-01, 4.92865310e-01, 5.83657533e00],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [-9.08334125e-01, 2.45730618e-01, 3.38445831e-01, -1.24839552e01],
         [3.85086813e-01, 8.07132590e-01, 4.47487573e-01, -3.09458670e00],
         [-1.63209262e-01, 5.36799260e-01, -8.27773696e-01, 3.92606379e-01],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [-9.67348739e-01, 1.21842398e-01, 2.22240517e-01, -1.85704401e01],
         [1.41335105e-01, -4.68537759e-01, 8.72064652e-01, 2.49347607e00],
         [2.10382522e-01, 8.75001028e-01, 4.36018802e-01, -2.85103157e00],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [-9.68131094e-01, 2.36140964e-01, 8.34243929e-02, -2.56624122e01],
         [-2.50185180e-01, -8.96757910e-01, -3.65010446e-01, 5.78289856e00],
         [-1.13824344e-02, -3.74249510e-01, 9.27258187e-01, 1.35331887e00],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [8.33388929e-01, 4.65372766e-01, -2.98146075e-01, -2.21959944e01],
         [2.06389223e-01, 2.38378208e-01, 9.48988577e-01, 1.38533258e01],
         [5.12704966e-01, -8.52410710e-01, 1.02613836e-01, 9.42938813e00],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [4.74592228e-01, 8.29146776e-02, 8.76291831e-01, -2.30495364e01],
         [1.06946866e-01, -9.93609385e-01, 3.60937412e-02, 4.88500517e00],
         [8.73684488e-01, 7.65868556e-02, -4.80426756e-01, 1.72528118e01],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [4.45591832e-01, 8.74747034e-01, -1.90435148e-01, -2.72265245e01],
         [5.29523139e-01, -8.60116643e-02, 8.43923716e-01, -1.99056460e00],
         [7.21840123e-01, -4.76885332e-01, -5.01524891e-01, 1.35015131e01],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [-8.96340647e-01, 1.82566910e-01, -4.04033127e-01, -2.47340966e01],
         [2.89369675e-01, -4.49539679e-01, -8.45091278e-01, -7.08898174e00],
         [-3.35914625e-01, -8.74404598e-01, 3.50111359e-01, 9.25244351e00],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [-5.50186575e-01, 5.15810773e-01, 6.56684079e-01, -1.83823376e01],
         [-3.02246289e-01, -8.56098432e-01, 4.19216717e-01, -1.19978602e01],
         [7.78422709e-01, 3.21670835e-02, 6.26915756e-01, 1.58220739e00],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [-6.10980528e-01, -2.50872711e-01, -7.50843311e-01, -1.20752113e01],
         [-5.47438746e-01, -5.51234221e-01, 6.29644069e-01, -1.60878799e01],
         [-5.71851042e-01, 7.95740986e-01, 1.99455932e-01, -2.28278627e00],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [6.49355761e-01, 2.79918046e-01, 7.07094749e-01, -1.16759454e01],
         [6.11370984e-01, -7.45129011e-01, -2.66473784e-01, -1.87048111e01],
         [4.52285989e-01, 6.05333499e-01, -6.54987587e-01, 6.07875186e00],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [1.92516767e-01, 9.66824042e-01, 1.67894509e-01, -1.37542204e01],
         [5.69741897e-01, -2.49430960e-01, 7.83057065e-01, -3.20980371e01],
         [7.98956485e-01, -5.50950781e-02, -5.98859806e-01, 8.85284656e00],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [-2.45787768e-02, 5.51087518e-01, -8.34085386e-01, -8.35234440e00],
         [-7.76142285e-01, 5.15337781e-01, 3.63359498e-01, -3.67354844e01],
         [6.30078596e-01, 6.56299870e-01, 4.15055953e-01, 4.29652148e00],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
      [
         [-5.91181079e-01, -4.32369907e-01, -6.80853284e-01, -1.53550889e00],
         [6.19913637e-01, 2.96440221e-01, -7.26519289e-01, -2.61030034e01],
         [5.15957376e-01, -8.51574694e-01, 9.27821522e-02, 8.72953632e00],
         [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
      ],
   ],
])
