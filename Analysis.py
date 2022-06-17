from math import cos, sin, acos, asin, degrees, radians, sqrt
from Configuration import Mechanism

class State:
    def __init__(self, mechanism:Mechanism, x, y) -> None:
        self.mech = mechanism
        self.fx = x
        self.fy = y

    def analyze_points(self):
        m = self.mech
        self.ex = self.fx - m.lef * cos(radians(m.beta3))
        self.ey = self.fy - m.lef * sin(radians(m.beta3))
        self.dx = self.ex - m.lde
        self.dy = self.ey 
        self.cx = self.dx - m.lcd
        self.cy = self.dy
        self.alpha1 = self.calculate_alpha1(m)
        self.alpha2 = self.calculate_alpha2(m)
        self.bx = m.lab * cos(radians(self.alpha1))
        self.by = m.lab * sin(radians(self.alpha1))
        self.gx = m.lag * cos(radians(self.alpha2))
        self.gy = m.lag * cos(radians(self.alpha2))

    def analyze_pressure_angles(self):
        pass
        
    def calculate_alpha1(self, m:Mechanism):
        # Equation here based on lbc
        rhs_bc = (m.lab**2 - m.lbc**2 + self.cx**2 + self.cy**2)/(2*m.lab)
        alpha1_cand = solve_alpha(self.cx, self.cy, rhs_bc)
        if alpha1_cand is None:
            print('Error: No Possible Resolution')
            return
        for value in alpha1_cand:
            bx = m * cos(radians(value))
            if bx >= self.cx:
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
        rhs_dg = (m.lag**2 - m.ldg**2 + self.dx**2 + self.dy**2)/(2*m.lag)
        alpha2_cand = solve_alpha(self.dx, self.dy, rhs_dg)
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