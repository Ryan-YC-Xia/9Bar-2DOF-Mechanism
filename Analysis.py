from math import cos, sin, acos, asin, degrees, radians, sqrt


class Mechanism:
    def __init__(self) -> None:
        self.lab = 130.000
        self.lbc = 50.000
        self.lcd = 27.500
        self.lde = self.lhm = self.lan = 0
        self.lef = 172.500
        self.ldg = self.lek = 147.022
        self.lag = self.lnk = 60.000
        self.lah = self.lnm = 45.000
        self.beta1 = self.beta2 = 90
        self.beta3 = 0

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
        # Equation here based on lbc and ldg
        rhs_bc = (m.lab**2 - m.lbc**2 + self.cx**2 + self.cy**2)/(2*m.lab)
        rhs_dg = (m.lag**2 - m.ldg**2 + self.dx**2 + self.dy**2)/(2*m.lag)
        alpha1 = solve_alpha(self.cx, self.cy, rhs_bc)
        alpha2 = solve_alpha(self.dx, self.dy, rhs_dg)
        if alpha1 is None or alpha2 is None:
            print('Error: No Possible Resolution')
        

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



