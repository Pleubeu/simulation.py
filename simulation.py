# 
# Simulation du mouvement d'oscillation
#
# Groupe 11.61
#
from math import sin, cos, tan , pi, atan
import matplotlib.pyplot as plt
import numpy as np
from gui import Interface, gui_launcher

### Constantes
g = 9.81                # gravitation [m/s²]

### paramètres propres à notre grue :
h = 0.09                # hauteur de la plateforme flottante    [m]
mtot = 2.9              # masse totale                          [kg]  
l = 0.58                # longueur de la plateforme flottante   [m]
inertie = 2.22          # Moment d'inertie                      [kg/m²]
g2 = 0.05               # hauteur du centre de gravité          [m]
D = 2                   # coefficient d'amortissement

### Paramètres variables 
mc = 0.2                # masse de la charge portée             [kg]
d_mc = 0.7              # distance du centre à la charge        [m]
v_mc = 1                # vitesse de déplacement de la charge   [m/s]
angle_0 = -0.03         # angle initial (calculé lors du concours) [rad]

### Interface graphique pour redéfinir les paramètres variables
dic_values = {"mc": mc, "d_mc": d_mc, "v_mc": v_mc, "angle_0": angle_0}
interface = gui_launcher(dic_values)        # lancement de l'interface graphique pour définir les paramètres
mc = interface.mc
d_mc = interface.d_mc
v_mc = interface.v_mc
angle_0 = interface.angle_0

### Valeurs calculées sur base des paramètres définis ci-dessus
hc = mtot / (l*l*260)                 # enfoncement de la plateforme                    [m]
a_submersion = atan((h-hc)/(l/2))     # angle de submersion de la plateforme            [rad]
a_soulevement = atan(hc/(l/2))        # angle de soulèvement de la plateforme           [rad]

### Paramètres de la simulation
step = 0.001            # step (dt)                     [s]
end = 10                # durée                         [s]
v_0 = 0.0               # vitesse angulaire initiale    [rad/s]

### Création des 'arrays' numpy, utilisés pour la simulation
t = np.arange(0, end, step)         # array de type : [0.0000e+00 1.0000e-04 2.0000e-04 ... 3.9997e+00 3.9998e+00 3.9999e+00]
angle = np.empty_like(t)            # array de type : [0. 0. 0. ... 0. 0. 0.] de même longueur que t
v = np.empty_like(t)
a = np.empty_like(t)
dist_mc = np.empty_like(t)
cc = np.empty_like(t)
cr = np.empty_like(t)
E_G = np.empty_like(t)
E_C = np.empty_like(t)
E_A = np.empty_like(t)
E_K = np.empty_like(t)

def dist():
    """
    Pre: -
    Post: compléte le array 'dist_mc' pour simuler une charge à distance variable
    """
    dt = step
    for i in range(len(dist_mc)-1):
        if dist_mc[i] < d_mc:
            dist_mc[i+1] = dist_mc[i] + v_mc * dt
        else:
            dist_mc[i+1] = d_mc

def simulation():
    """
    pre: -
    post: exécute une simulation jusqu'à t=end par pas de dt=step.
          Remplit les listes x, v, a des positions, vitesses et accélérations.
    """
    # conditions et paramètres initiaux
    angle[0] = angle_0
    v[0] = v_0
    dt = step 
    
    for i in range(len(t)-1):                   # pour chaque élément de l'array t ==> calcul de angle, v et a pour chaque dt

        ### calcul du C = Couple résultant = Couple de chavirement + couple de redressement :
        d_cg = ((sin(angle[i])) * l)  /  ( 12 * hc * (cos(angle[i]**2)))  - ( g2 * sin(angle[i]) )  #calcul de dist(C', G'), en fonction de angle
        cr[i] = -( mtot * g * d_cg )            # calcul du couple de redressement, négatif car anti-horaire
        cc[i] = (mc * dist_mc[i] * g )          # calcul du couple de chavirement
        couple = cc[i] + cr[i]                  # calcul du C

        ### calcul accélération, vitesse, angle
        a[i] = (-D*v[i] + couple) / inertie     #calcul de l'accélération angulaire selon la formule donnée : I * a = -D * v + C
        v[i+1] = v[i] + a[i] * dt               #calcul vitesse angulaire en fonction de a
        angle[i+1] = angle[i] + v[i] * dt       #calcul angle en fonction de v
        
    a[-1] = a[-2]   # on fixe la dernière valeur de a, qui serait sinon restée à 0 (qui vient de l'initialisation de l'array)

# Fonctions pour calculer le graphique des différents angles finaux en fonction du poids de la charge et de la distance
def eq(a, m, d):
    """
    Pre :   a = nombre : l'angle (en radian)
            m = nombre : la masse de la charge
            d = nombre :  la distance de la charge au centre
    Post :  retourne un nombre : résultat de l'équation
    """
    angle = a # Cc = Cr ==> mc * g * d = mtot * g * dc'g' ==> dc'g' = (mc * d) / mtot ==> dc'g' - (mc * d) = 0
    eq_l = ( ( l* (sin(angle)) / ( 12 * hc * (cos(angle)**2)) ) - ( g2 * sin(angle) ) ) - ( (m * d) / (mtot) )
    return eq_l

def dichotomic_sol(m, d=2):
    """
    Pre : m = nombre : masse de la charge
    Post : retourne un nombre : l'angle (en radian) à l'équilibre
    """
    p=5
    precision = 10**(-p)
    angle1 = 0
    angle2 = pi/2
    a_precision = 10
    while abs(a_precision) > precision:     # recherche dichotomique de l'angle final, pour une précison donnée
        angle_mid = (angle1 + angle2 )/2    # on divise l'intervalle en deux
        try_mid = eq(angle_mid, m, d)       # et on prend le demi-intervalle qui contient la solution
        if try_mid > 0:                     # (==> pour lequel les deux bornes sont de signes opposés)
            angle2 = angle_mid  
        elif try_mid < 0:
            angle1 = angle_mid
        a_precision = angle1 - angle2
    angle_mid = (angle1 + angle2) /2
    return round(angle_mid*180/pi, p)


def graphiques():
    """
    Création de 4 fenêtres avec :
    1 : angle / t, vitesse / t et accélération / t
    2 : distance de la charge / t et énergie / t
    3 : diagramme de phase (vitesse / angle)
    4 : angle / distance de la charge (pour charges de masse différentes)
    """
    ### première fenêtre
    plt.figure(1)           
    plt.subplot(3,1,1)      # graphique = angle / t
    plt.plot(t,angle*180/pi, label="angle")
    plt.plot([0, end], [a_soulevement*180/pi, a_soulevement*180/pi], label="soulèvement", color="red", ls="--")
    plt.plot([0, end], [a_submersion*180/pi, a_submersion*180/pi], label="submersion", color="magenta", ls="--")
    plt.plot([0, end], [-a_soulevement*180/pi, -a_soulevement*180/pi], color="red", ls="--")
    plt.plot([0, end], [-a_submersion*180/pi, -a_submersion*180/pi], color="magenta", ls="--")
    plt.ylabel("angle [°]")
    plt.legend(loc="upper right")
    plt.subplot(3,1,2)      # graphique = vitesse / t
    plt.plot(t,v*180/pi, label="vitesse")
    plt.ylabel("vitesse [°/s]")
    plt.legend()
    plt.subplot(3,1,3)      # graphique = accélération / t
    plt.plot(t,a*180/pi, label="accelération", color="black")
    plt.ylabel("accelération [°/s²]")
    plt.xlabel("temps [s]")
    plt.legend()
    plt.show()

    ### Deuxième fenêtre
    plt.figure(1)           
    plt.subplot(1,1,1)      # graphique = dist_mc / t
    plt.plot(t,dist_mc, label="dist mc", color="black")
    plt.ylabel("distance de la charge [m]")
    plt.legend()
    plt.show()

    ### Troisième fenêtre
    plt.figure(3)
    plt.subplot(1,1,1)      # graphique diagramme de phase = angle / omega
    plt.title("Diagramme de phase")
    plt.plot(angle*180/pi,v*180/pi)
    plt.ylabel("vitesse [°/s]")
    plt.xlabel("angle [°]")
    plt.show()

    ### quatrième fenêtre
    g_end=2
    m=[0.1 ,0.2, 0.3, 0.4]
    c=["red","blue","black","green","yellow"]
    plt.figure(4)           # graphique des angles finaux / dist_mc, pour plusieurs mc différents
    plt.xlabel("distance [m]")
    plt.ylabel("inclinaison [°]")
    plt.plot([0, g_end], [a_soulevement*180/pi, a_soulevement*180/pi], label="soulèvement", color="red", ls="--")
    plt.plot([0, g_end], [a_submersion*180/pi, a_submersion*180/pi], label="submersion", color="magenta", ls="--")
    for i in range(len(m)) :
        plt.plot( [0, g_end] , [0, dichotomic_sol( m[i])] , color=c[i] , label="m={0} kg".format(m[i]))  
    plt.legend()
    plt.show()    


################################################################################
###  Programme principal :
# appel des fonction dist, simulation et graphiques
# imprime l'angle final = obtenu à la fin de la simulation
dist()
simulation()
print("angle final = ", round(angle[-1], 5), "rad = ", round(angle[-1]*180/pi, 5), "°")
graphiques()