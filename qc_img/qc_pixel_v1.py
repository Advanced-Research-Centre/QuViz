from qiskit import QuantumCircuit

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

def plt_qc_pixel(qc):

    cmap = plt.get_cmap('Dark2')
    # cmap = plt.get_cmap('gist_rainbow')
    c_nos = 8
    c_vals = cmap(np.linspace(0, 1, c_nos))  # try 'Set2' for pastel version, both support upto 8 gates
    c_nos_assigned = 0

    gate_color_dict = {}  
    h = qc.num_qubits + qc.num_clbits
    w = sum(qc.count_ops().values())    # Note: not qc.depth() 
    # g_depth = 0
    # for g in qc:
    #     gate = g.name
    #     if gate not in gate_color_dict.keys():
    #         gate_color_dict[gate] = []
    #         tgt = len(g.qubits) + len(g.clbits)
    #         for q in range(tgt):
    #             gate_color_dict[gate].append(c_nos_assigned)
    #             c_nos_assigned = (c_nos_assigned + 1) 
    #             # if c_nos_assigned == c_nos:
    #             #     print("All colours assigned, colors will be reused. To prevent, increase c_nos and/or choose a different color map")
    #             #     c_nos_assigned %= c_nos
    #     for q in range(len(g.qubits)):
    #         qc_img[g.qubits[q]._index][g_depth][:] = gate_color_dict[gate][q]
    #     for q in range(len(g.clbits)):
    #         qc_img[qc.num_qubits + g.clbits[q]._index][g_depth][:] = gate_color_dict[gate][len(g.qubits)+q]
    #     g_depth += 1



    qc_img = np.ones((h, w, 3), dtype=np.uint8)*255

    g_depth = 0
    for g in qc:
        gate = g.name
        if gate not in gate_color_dict.keys():
            gate_color_dict[gate] = []
            tgt = len(g.qubits) + len(g.clbits)
            for q in range(tgt):
                gate_color_dict[gate].append([int(c) for c in c_vals[c_nos_assigned][:-1]*255])
                c_nos_assigned = (c_nos_assigned + 1) 
                if c_nos_assigned == c_nos:
                    print("All colours assigned, colors will be reused. To prevent, increase c_nos and/or choose a different color map")
                    c_nos_assigned %= c_nos
        for q in range(len(g.qubits)):
            qc_img[g.qubits[q]._index][g_depth][:] = gate_color_dict[gate][q]
        for q in range(len(g.clbits)):
            qc_img[qc.num_qubits + g.clbits[q]._index][g_depth][:] = gate_color_dict[gate][len(g.qubits)+q]
        g_depth += 1

    scale_h = 100
    scale_w = 100

    qc_img_scaled = np.zeros((h*scale_h, w*scale_w, 3), dtype=np.uint8)

    for i in range(h):
        for j in range(w):
            qc_img_scaled[i*scale_h:(i+1)*scale_h,j*scale_w:(j+1)*scale_w] = qc_img[i][j]

    img = Image.fromarray(qc_img_scaled, 'RGB')
    img.save('demo_plots/qc.png')
    img.show()

# from qiskit.qasm2 import dumps
qc = QuantumCircuit(3,1)
qc.reset([0,1,2])
qc.h(0)
qc.cx(0,1)
qc.h(1)
qc.cx(1,0)
qc.cz(2,0)
qc.t(2)
qc.measure(1,0)
# print(dumps(qc))

plt_qc_pixel(qc)