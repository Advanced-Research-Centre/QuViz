# https://www.giss.nasa.gov/tools/gprojector/help/projections/

import numpy as np
import math
from matplotlib import pyplot as plt

h = np.array([[1,1],[1,-1]], dtype=complex) / np.sqrt(2)
t = np.array([[1,0],[0,np.exp(1j*np.pi/4)]], dtype=complex)
# tdg = np.array([[1,0],[0,np.exp(-1j*np.pi/4)]], dtype=complex)
gs = {'h':[h,'b-'],'t':[t,'g-']}

# Use a dark background
# plt.style.use('dark_background')

# Set a figure
plt.figure(figsize=(12, 8))

# Apply the aitoff projection and activate the grid
plt.subplot(projection="aitoff")
plt.grid(True)

# Set long. / lat. labels
# plt.xlabel('Long. in deg')
# plt.ylabel('Lat. in deg')

psi_0 = np.array([[1,0]], dtype=complex).T
psi = [[psi_0,psi_0,'b-']]   # from, to

def get_spherical_coordinates(statevector):
    # Convert to polar form:
    r0 = np.abs(statevector[0])
    ϕ0 = np.angle(statevector[0])

    r1 = np.abs(statevector[1])
    ϕ1 = np.angle(statevector[1])

    # Calculate the coordinates:
    r = np.sqrt(r0 ** 2 + r1 ** 2)
    θ = 2 * np.arccos(r0 / r)
    ϕ = ϕ1 - ϕ0
    return [r, θ, ϕ]

level = 1
for i in range(level):
    psi_nxt = []
    for s in psi:
        [r, θ, ϕ] = get_spherical_coordinates(s[1])
        # print(s[1],'\n')
        lat = np.pi/2 - θ
        lon = ϕ 
        # print(lat,lon)
        plt.plot(lon, lat, color='r', marker='o', linestyle='None', markersize=7)
        
        [r0, θ0, ϕ0] = get_spherical_coordinates(s[0])
        lat0 = np.pi/2 - θ0
        lon0 = ϕ0 
        plt.plot([lon0,lon], [lat0,lat], s[2], linewidth = 2.0)
        for u in gs.keys():
            psi_nxt.append([s[1],np.dot(gs[u][0],s[1]),gs[u][1]])
    psi = psi_nxt

# Save the figure
plt.savefig('ht_'+str(level)+'_0.png', dpi=300)

# plt.show()

# rho_0 = np.outer(psi_0,psi_0)
# rho = [rho_0]
# for i in range(level):
#     rho_nxt = []
#     for s in rho:
#         a = s[0, 0]
#         b = s[1, 0]
#         x = 2.0 * b.real
#         y = 2.0 * b.imag
#         z = 2.0 * a - 1.0
#         R = 1
#         print(z)
#         lat = math.asin(z.real / R)
#         lon = math.atan2(y, x)
#         plt.plot(lon, lat, color='r', marker='o', linestyle='None', markersize=4)
#         # plt.plot(x[i:i+2], y[i:i+2], 'ro-')
#         for u in gs:
#             rho_nxt.append(np.dot(u,np.dot(s,u.conj().T)))
#     rho = rho_nxt
# plt.show()
