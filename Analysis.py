from math import cos, sin, acos, asin, degrees, radians, sqrt, atan2
from Configuration import Mechanism

class State:
    def __init__(self, mechanism:Mechanism, x, y) -> None:
        self.mech = mechanism
        self.f = (x, y)

    def analyze(self):
        # Points
        m = self.mech
        self.a = (0, 0)
        self.e = (self.f[0] - m.lef * cos(radians(m.beta3)), self.f[1] - m.lef * sin(radians(m.beta3)))
        self.d = (self.e[0] - m.lde, self.e[1])
        self.c = (self.d[0] - m.lcd, self.d[1])
        self.alpha1 = self.calculate_alpha1(m)
        self.alpha2 = self.calculate_alpha2(m)
        self.b = (m.lab * cos(radians(self.alpha1)), m.lab * sin(radians(self.alpha1)))
        self.g = (m.lag * cos(radians(self.alpha2)), m.lag * cos(radians(self.alpha2)))
        self.h = (m.lah * cos(radians(self.alpha2 - m.beta1)), m.lah * sin(radians(self.alpha2 - m.beta1)))
        self.m = (self.h[0] + m.lan, self.h[1])
        self.n = (self.a[0] + m.lan, self.a[1])
        self.k = (self.g[0] + m.lan, self.g[1])
        # Pressure Angles
        self.abc = calculate_angle(self.a, self.b, self.c)
        self.cdg = calculate_angle(self.c, self.c, self.g)
        self.agd = calculate_angle(self.a, self.g, self.d)
        self.ahm = calculate_angle(self.a, self.h, self.m)
        
    def calculate_alpha1(self, m:Mechanism):
        # Equation here based on lbc
        rhs_bc = (m.lab**2 - m.lbc**2 + self.c[0]**2 + self.c[1]**2)/(2*m.lab)
        alpha1_cand = solve_alpha(self.c[0], self.c[1], rhs_bc)
        if alpha1_cand is None:
            print('Error: No Possible Resolution')
            return
        for value in alpha1_cand:
            bx = m * cos(radians(value))
            if bx >= self.c[0]:
                alpha1_cand.remove(value)
        if len(alpha1_cand) == 0:
            print('Error: No valid alpha1 value')
            return
        if len(alpha1_cand) > 1:
            print('Error: Fail to obtain sole solution for alpha1')
            return
        return alpha1_cand[0]

    def calculate_alpha2(self, m:Mechanism):
        # Equation here based on ldg
        rhs_dg = (m.lag**2 - m.ldg**2 + self.d[0]**2 + self.d[1]**2)/(2*m.lag)
        alpha2_cand = solve_alpha(self.d[0], self.d[1], rhs_dg)
        if alpha2_cand is None:
            print('Error: No Possible Resolution')
            return
        for value in alpha2_cand:
            if value >= 90 and value <= 270:
                alpha2_cand.remove(value)
        if len(alpha2_cand) == 0:
            print('Error: No valid alpha2 value')
            return
        if len(alpha2_cand) > 1:
            print('Error: Fail to obtain sole solution for alpha2')
            return
        return alpha2_cand[0]

#
# Helper Functions for caculating angles
#

# Function solves numerically equations of form 'a*cos(alpha) + b*sin(alpha) = c'
def solve_alpha(a, b, c):
    den = sqrt(a**2 + b**2)
    theta = solve_theta(b/den, a/den)
    if abs(c/den) > 1:
        return None
    asum = solve_asum(c/den)   
    alpha = [a - theta for a in asum]
    return alpha

def solve_theta(cos_t, sin_t):
    theta = degrees(acos(abs(cos_t)))
    if cos_t >= 0 and sin_t >= 0:
        return theta
    if cos_t < 0 and sin_t > 0:
        return 180-theta
    if cos_t < 0 and sin_t < 0:
        return 180+theta
    if cos_t > 0 and sin_t < 0:
        return 360-theta
    return None

def solve_asum(sin_v):
    angle = degrees(asin(abs(sin_v)))
    asum = []
    if sin_v >= 0:
        asum.append(angle)
        asum.append(180-angle)
    else:
        asum.append(180-angle)
        asum.append(360+angle)
    return asum

# Calculate the angle given three points
def calculate_angle(a, b, c):
        ang = degrees(atan2(c[1]-b[1], c[0]-b[0]) - atan2(a[1]-b[1], a[0]-b[0]))
        return abs(ang)