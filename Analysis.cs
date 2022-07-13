namespace Namespace {
    
    using cos = math.cos;
    
    using sin = math.sin;
    
    using acos = math.acos;
    
    using asin = math.asin;
    
    using degrees = math.degrees;
    
    using radians = math.radians;
    
    using sqrt = math.sqrt;
    
    using atan2 = math.atan2;
    
    using Mechanism = Configuration.Mechanism;
    
    using System;
    
    using System.Linq;
    
    using System.Collections.Generic;
    
    public static class Module {
        
        public class State {
            
            public State(object mechanism = Mechanism, object x, object y) {
                this.mech = mechanism;
                this.f = (x, y);
            }
            
            public virtual object analyze() {
                // Points
                var m = this.mech;
                this.a = (0, 0);
                this.e = (this.f[0] - m.lef * cos(radians(m.beta3)), this.f[1] - m.lef * sin(radians(m.beta3)));
                this.d = (this.e[0] - m.lde, this.e[1]);
                this.c = (this.d[0] - m.lcd, this.d[1]);
                this.alpha1 = this.calculate_alpha1(m);
                this.alpha2 = this.calculate_alpha2(m);
                this.b = (m.lab * cos(radians(this.alpha1)), m.lab * sin(radians(this.alpha1)));
                this.g = (m.lag * cos(radians(this.alpha2)), m.lag * cos(radians(this.alpha2)));
                this.h = (m.lah * cos(radians(this.alpha2 - m.beta1)), m.lah * sin(radians(this.alpha2 - m.beta1)));
                this.m = (this.h[0] + m.lan, this.h[1]);
                this.n = (this.a[0] + m.lan, this.a[1]);
                this.k = (this.g[0] + m.lan, this.g[1]);
                // Pressure Angles
                this.abc = calculate_angle(this.a, this.b, this.c);
                this.cdg = calculate_angle(this.c, this.c, this.g);
                this.agd = calculate_angle(this.a, this.g, this.d);
                this.ahm = calculate_angle(this.a, this.h, this.m);
            }
            
            public virtual object calculate_alpha1(object m = Mechanism) {
                // Equation here based on lbc
                var rhs_bc = (Math.Pow(m.lab, 2) - Math.Pow(m.lbc, 2) + Math.Pow(this.c[0], 2) + Math.Pow(this.c[1], 2)) / (2 * m.lab);
                var alpha1_cand = solve_alpha(this.c[0], this.c[1], rhs_bc);
                if (alpha1_cand == null) {
                    Console.WriteLine("Error: No Possible Resolution");
                    return;
                }
                foreach (var value in alpha1_cand) {
                    var bx = m * cos(radians(value));
                    if (bx >= this.c[0]) {
                        alpha1_cand.remove(value);
                    }
                }
                if (alpha1_cand.Count == 0) {
                    Console.WriteLine("Error: No valid alpha1 value");
                    return;
                }
                if (alpha1_cand.Count > 1) {
                    Console.WriteLine("Error: Fail to obtain sole solution for alpha1");
                    return;
                }
                return alpha1_cand[0];
            }
            
            public virtual object calculate_alpha2(object m = Mechanism) {
                // Equation here based on ldg
                var rhs_dg = (Math.Pow(m.lag, 2) - Math.Pow(m.ldg, 2) + Math.Pow(this.d[0], 2) + Math.Pow(this.d[1], 2)) / (2 * m.lag);
                var alpha2_cand = solve_alpha(this.d[0], this.d[1], rhs_dg);
                if (alpha2_cand == null) {
                    Console.WriteLine("Error: No Possible Resolution");
                    return;
                }
                foreach (var value in alpha2_cand) {
                    if (value >= 90 && value <= 270) {
                        alpha2_cand.remove(value);
                    }
                }
                if (alpha2_cand.Count == 0) {
                    Console.WriteLine("Error: No valid alpha2 value");
                    return;
                }
                if (alpha2_cand.Count > 1) {
                    Console.WriteLine("Error: Fail to obtain sole solution for alpha2");
                    return;
                }
                return alpha2_cand[0];
            }
        }
        
        //
        // Helper Functions for caculating angles
        //
        // Function solves numerically equations of form 'a*cos(alpha) + b*sin(alpha) = c'
        public static object solve_alpha(object a, object b, object c) {
            var den = sqrt(Math.Pow(a, 2) + Math.Pow(b, 2));
            var theta = solve_theta(b / den, a / den);
            if (abs(c / den) > 1) {
                return null;
            }
            var asum = solve_asum(c / den);
            var alpha = (from a in asum
                select (a - theta)).ToList();
            return alpha;
        }
        
        public static object solve_theta(object cos_t, object sin_t) {
            var theta = degrees(acos(abs(cos_t)));
            if (cos_t >= 0 && sin_t >= 0) {
                return theta;
            }
            if (cos_t < 0 && sin_t > 0) {
                return 180 - theta;
            }
            if (cos_t < 0 && sin_t < 0) {
                return 180 + theta;
            }
            if (cos_t > 0 && sin_t < 0) {
                return 360 - theta;
            }
            return null;
        }
        
        public static object solve_asum(object sin_v) {
            var angle = degrees(asin(abs(sin_v)));
            var asum = new List<object>();
            if (sin_v >= 0) {
                asum.append(angle);
                asum.append(180 - angle);
            } else {
                asum.append(180 - angle);
                asum.append(360 + angle);
            }
            return asum;
        }
        
        // Calculate the angle given three points
        public static object calculate_angle(object a, object b, object c) {
            var ang = degrees(atan2(c[1] - b[1], c[0] - b[0]) - atan2(a[1] - b[1], a[0] - b[0]));
            return abs(ang);
        }
    }
}