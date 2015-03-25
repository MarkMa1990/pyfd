import numpy as np

def product_difference(m):
    N = int(m.size / 2)

    Pn = 2*N+1

    P = np.zeros((Pn, Pn))
    P[0,0] = 1
    for i in range(Pn-1):
        P[i,1] = (-1)**i*m[i]
    for j in range(2,Pn):
        for i in range(Pn+1-j):
            P[i,j]=P[0,j-1]*P[i+1,j-2]-P[0,j-2]*P[i+1,j-1]

    zeta = np.concatenate(([0],P[0,2:2*N+1]/(P[0,1:2*N]*P[0,:2*N-1])))

    a = zeta[0::2]+zeta[1::2]
    b = zeta[1:-1:2]*zeta[2::2]

    b_diag = -np.sqrt(np.abs(b))
    jacobi = np.diag(a) + np.diag(b_diag, k=1) + np.diag(b_diag, k=-1)

    eigval, eigvec = np.linalg.eig(jacobi)
    w = m[0] * eigvec[0, :]**2

    return eigval, w




def wheeler_inversion(m):
    N = int(m.size / 2)  # number of nodes of the quadrature approximation

    sigma = np.zeros((N+1, 2*N))
    sigma[1, :] = m[0:2*N]

    a = np.zeros(N)
    b = np.zeros(N)
    a[0] = m[1] / m[0]
    b[0] = m[0]  # This value is insignificant as it's not being used.

    for k in range(1, N):
        l = np.arange(2*(N - k)) + k
        sigma[k+1, l] = sigma[k, l+1] - a[k-1]*sigma[k, l] - \
            b[k-1]*sigma[k-1, l]

        a[k] = -sigma[k, k] / sigma[k, k-1] + \
            sigma[k+1, k+1] / sigma[k+1, k]

        b[k] = sigma[k+1, k] / sigma[k, k-1]

    b_diag = -np.sqrt(np.abs(b[1:]))
    jacobi = np.diag(a) + np.diag(b_diag, k=1) + np.diag(b_diag, k=-1)

    eigval, eigvec = np.linalg.eig(jacobi)
    w = m[0] * eigvec[0, :]**2

    return eigval, w


def is_realizable(m):
    N = int(m.size/2)
    M = np.zeros((N, N))
    for i in range(0, N):
        M[i, :] = m[i:N+i]
    for l in range(1, N):
        if (np.linalg.det(M[0:l, 0:l]) < 0):
            return False
    for l in range(2, N-1):
        if (np.linalg.det(M[1:l, 1:l]) < 0):
            return False

    return True
