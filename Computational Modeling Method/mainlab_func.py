import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def MAPK_model(y, t, params):
    # 파라미터 언팩
    V1, n, Ki, K1 = params[0], params[1], params[2], params[3]
    V2, K2 = params[4], params[5]
    k3, K3 = params[6], params[7]
    k4, K4 = params[8], params[9]
    V5, K5 = params[10], params[11]
    V6, K6 = params[12], params[13]
    k7, K7 = params[14], params[15]
    k8, K8 = params[16], params[17]
    V9, K9 = params[18], params[19]
    V10, K10 = params[20], params[21]

    # Unpack variables
    MKKK_P = y[0]
    MKK_P = y[1]
    MKK_PP = y[2]
    MAPK_P = y[3]
    MAPK_PP = y[4]

    MKKK = 100 - MKKK_P
    MKK = 300 - MKK_P - MKK_PP
    MAPK = 300 - MAPK_P - MAPK_PP

    # Reaction rates
    v1 = V1 * MKKK / ((1 + (MAPK_PP / Ki) ** n) * (K1 + MKKK))  # allosteric inhibition : negative feedback
    # v1 = V1 * MKKK / (K1 + MKKK)
    v2 = V2 * MKKK_P / (K2 + MKKK_P)
    v3 = k3 * MKKK_P * MKK / (K3 + MKK)
    v4 = k4 * MKKK_P * MKK_P / (K4 + MKK_P)
    v5 = V5 * MKK_PP / (K5 + MKK_PP)
    v6 = V6 * MKK_P / (K6 + MKK_P)
    v7 = k7 * MKK_PP * MAPK / (K7 + MAPK)
    v8 = k8 * MKK_PP * MAPK_P / (K8 + MAPK_P)
    v9 = V9 * MAPK_PP / (K9 + MAPK_PP)
    v10 = V10 * MAPK_P / (K10 + MAPK_P)

    # ODEs
    #dMKKK = v2 -v1
    dMKKK_P = v1 - v2
    #dMKK = v6 - v3
    dMKK_P = v3 + v5 - v4 - v6
    dMKK_PP = v4 - v5
    #dMAPK = v10 - v7
    dMAPK_P = v7 + v9 - v8 - v10
    dMAPK_PP = v8 - v9

    return [dMKKK_P, dMKK_P, dMKK_PP, dMAPK_P, dMAPK_PP]

# Parameters
params = [
    2.5, 1, 9, 10,        # V1, n, Ki, K1
    0.25, 8,              # V2, K2
    0.025, 15,            # k3, K3
    0.025, 15,            # k4, K4
    0.75, 15,             # V5, K5
    0.75, 15,             # V6, K6
    0.025, 15,            # k7, K7
    0.025, 15,            # k8, K8
    0.5, 15,              # V9, K9
    0.5, 15               # V10, K10
]