from manim import *

class RegressionVideo(ThreeDScene):
    def construct(self):

        # 1) Frase
        quote = Tex(
            r"``Todos los ",           
            r"modelos",                # CELESTE
            r" están ", 
            r"equivocados",
            r",\\",
            r"pero algunos son ",     
            r"útiles",                 # CELESTE
            r".''"                     
        )

        quote.scale(1.1).shift(UP * 0.5)

        for i in [1,6]:
            quote[i].set_color(BLUE)
        
        quote[3].set_color(RED)  # "equivocados"

        author = Text("- George E. P. Box", font="Serif", font_size=28)
        author.set_color(YELLOW)
        author.next_to(quote, DOWN, buff=0.8)


        self.play(Write(quote), run_time=2.5) 
        self.wait(0.2)
        self.play(FadeIn(author, shift=UP * 0.3), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(quote), FadeOut(author), run_time=0.5)


        # 2) Título
        title = Text(
            "¿Qué significa ajustar un modelo?",
            font_size=48, 
            t2c={"ajustar un modelo": TEAL} 
        )

        authors = Text(
            "por Mariana Capuñay",
            font_size=24,
            color=GRAY_B
        )

        title.to_edge(UP, buff=3)
        authors.next_to(title, DOWN, buff=1.0)

        self.play(Write(title), run_time=2.5)
        self.wait(0.2)
        self.play(FadeIn(authors, shift=UP), run_time=1)
        self.wait(1.5)

        self.play(
            FadeOut(title, shift=UP),
            FadeOut(authors, shift=UP),
            run_time=1.5
        )

        # 3) Regresión Lineal
        title = Text("Regresión Lineal", font_size=36)
        title.to_edge(UP) 

        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            x_length=7, 
            y_length=5,
            axis_config={
                "color": GREY, 
                "include_tip": False,
                "font_size": 24, # tamaño de números (en ejes)
            },
        )
        
        axes.add_coordinates(font_size=20)
        labels = axes.get_axis_labels(x_label="X", y_label="Y")

        # data: 
        x_vals = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        y_vals = [1.5, 2.1, 2.9, 4.2, 4.5, 5.8, 6.2, 7.8, 8.1]
        
        dots = VGroup()
        for x, y in zip(x_vals, y_vals):
            dots.add(Dot(axes.c2p(x, y), color=BLUE)) 

        self.play(Write(title), run_time=0.7)             
        self.play(Create(axes), Write(labels), run_time=1) 
        self.play(FadeIn(dots, lag_ratio=0.1), run_time=0.8) 
        self.wait(1) 


        # 4) Recta + fórmulas
        w_val = 0.86
        b_val = 0.48

        regression_line = axes.plot(lambda x: w_val * x + b_val, color=YELLOW)

        formula_text = MathTex(r"Y = w \cdot X + b", color=YELLOW, font_size=34) # fórmula: Y = wX + b
        formula_text.move_to(axes.c2p(2.5, 8.5))

        values_text = MathTex(
            f"w \\approx {w_val}", 
            f"\\quad b \\approx {b_val}", 
            font_size=28, 
            color=WHITE
        )
        values_text.next_to(formula_text, DOWN, buff=0.2)

        self.play(Create(regression_line), run_time=2)
        self.play(Write(formula_text))
        self.play(Write(values_text))
        self.wait(3) 

        
        # 5) Puntos rojos
        pred_x_vals = [0.5, 3.5, 7.5, 9.5]
        
        red_dots = VGroup()
        for x in pred_x_vals:
            y_pred = w_val * x + b_val 
            red_dots.add(Dot(axes.c2p(x, y_pred), color=RED))

        
        self.play(FadeIn(red_dots, scale=0.5), run_time=0.5) 
        
        for _ in range(4):
            self.play(
                red_dots.animate.set_opacity(0.2), 
                run_time=0.5
            )
            self.play(
                red_dots.animate.set_opacity(1),   
                run_time=0.5
            )

        self.play(FadeOut(red_dots), run_time=0.5) 


        # 5) Error
        errors = VGroup()
        for x, y in zip(x_vals, y_vals):
            y_pred = w_val * x + b_val
            linea = Line(
                start=axes.c2p(x, y),
                end=axes.c2p(x, y_pred),
                color=RED,
                stroke_width=3
            )
            errors.add(linea)

        idx_ej = 7
        x_i = x_vals[idx_ej]
        y_i = y_vals[idx_ej]
        y_p = w_val * x_i + b_val

        point_real = axes.c2p(x_i, y_i)
        point_pred = axes.c2p(x_i, y_p)

        prediction_dot = Dot(point_pred, color=YELLOW, radius=0.08)

        lbl_y = MathTex("y_i", color=BLUE, font_size=36)
        lbl_y.move_to(point_real + UP*0.7 + LEFT*0.7)

        arrow_y = Arrow(start=lbl_y.get_bottom(), end=point_real, buff=0.1, color=BLUE, stroke_width=3, tip_length=0.2)

        lbl_yp = MathTex(r"\hat{y}_i", color=YELLOW, font_size=36)
        lbl_yp.move_to(point_pred + DOWN*0.7 + RIGHT*0.7)

        arrow_yp = Arrow(start=lbl_yp.get_top(), end=prediction_dot.get_center(), buff=0.1, color=YELLOW, stroke_width=3, tip_length=0.2)

    
        self.play(Create(errors), run_time=2)
        self.wait(2)
        self.play(FadeIn(prediction_dot, scale=0.5), run_time=1)
        self.wait(1)

        self.play(
            Write(lbl_y), 
            Create(arrow_y), 
            run_time=2
        )
        
        self.wait(1)

        self.play(
            Write(lbl_yp), 
            Create(arrow_yp), 
            run_time=2
        )

        self.wait(4)

        # 6) Efecto con la recta: RECIEN AÑADIDO
        self.play(
            FadeOut(lbl_y, arrow_y, lbl_yp, arrow_yp, prediction_dot),
            run_time=0.5
        )

        w_tracker = ValueTracker(w_val) 
        
        def get_dynamic_group():
            x_max = 10
            w_now = w_tracker.get_value()
            
            new_line = Line(
                axes.c2p(0, b_val),
                axes.c2p(x_max, w_now * x_max + b_val),
                color=YELLOW,
                stroke_width=4
            )
            
            new_errors = VGroup()
            for x, y in zip(x_vals, y_vals):
                y_p_now = w_now * x + b_val
                linea = Line(
                    axes.c2p(x, y),
                    axes.c2p(x, y_p_now),
                    color=RED,
                    stroke_width=2,
                    stroke_opacity=0.6 # Un poco transparentes para que no sature
                )
                new_errors.add(linea)
            
            return VGroup(new_errors, new_line)

        dynamic_graph = always_redraw(get_dynamic_group)
        
        self.remove(regression_line, errors) 
        self.add(dynamic_graph)

        self.play(
            w_tracker.animate.set_value(w_val + 0.5), 
            run_time=2, 
            rate_func=linear
        )
        
        self.play(
            w_tracker.animate.set_value(w_val - 0.4), 
            run_time=2, 
            rate_func=linear
        )
        
        self.play(
            w_tracker.animate.set_value(w_val), 
            run_time=1.5, 
            rate_func=smooth 
        )
        
        self.remove(dynamic_graph)
        self.add(regression_line, errors)

        # 7) Error - fórmula
        error_label = Text("Error\nPromedio", font_size=22, color=RED_B, line_spacing=0.6)
        error_formula = MathTex(
            r"= \frac{1}{n} \sum (", 
            r"y_i", 
            r" - ", 
            r"\hat{y}_i", 
            r")^2",
            font_size=26, 
            color=RED_B
        )

        error_formula[1].set_color(BLUE)   # y_i
        error_formula[3].set_color(YELLOW) # y_hat_i

        error_group = VGroup(error_label, error_formula).arrange(RIGHT, buff=0.2)
        error_group.move_to(axes.c2p(7.5, 3))

        error_value = MathTex(r"= 0.06", font_size=26, color=RED_B)
        
        error_value.next_to(error_formula, DOWN, buff=0.4).align_to(error_formula, LEFT)

        self.play(Write(error_group), run_time=3.5) 
        self.play(Write(error_value), run_time=1.5) 

        self.wait(3)

        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.5
        )

        # 8) Creatures: Sumatoria y Productoria
        def crear_ojos(pupila_direction=ORIGIN, radio_pupila=0.05):
            ojo_blanco = Circle(radius=0.13, color=WHITE, fill_opacity=1, stroke_width=2)
            pupila = Dot(radius=radio_pupila, color=BLACK)
            pupila.shift(pupila_direction * 0.06)
            return VGroup(ojo_blanco, pupila)

        # Productoria (Pi)
        pi_symbol = MathTex(r"\Pi", font_size=180, color=TEAL)
        pi_ojo_l = crear_ojos(RIGHT)
        pi_ojo_r = crear_ojos(RIGHT)
        pi_ojos = VGroup(pi_ojo_l, pi_ojo_r).arrange(RIGHT, buff=0.05)
        pi_ojos.move_to(pi_symbol.get_top() + DOWN * 0.15)
        pi_boca = Arc(start_angle=PI, angle=-PI, radius=0.1, color=BLACK, stroke_width=3).scale(0.5).next_to(pi_ojos, DOWN, buff=0.1)
        
        pi_creature = VGroup(pi_symbol, pi_ojos, pi_boca).to_edge(LEFT, buff=3.0)

        # Sumatoria (Sigma)
        sigma_symbol = MathTex(r"\Sigma", font_size=180, color=BLUE)
        sigma_ojo_l = crear_ojos(UP + LEFT)
        sigma_ojo_r = crear_ojos(UP + LEFT)
        sigma_ojos = VGroup(sigma_ojo_l, sigma_ojo_r).arrange(RIGHT, buff=0.05)
        sigma_ojos.move_to(sigma_symbol.get_top() + RIGHT * 0.18 + DOWN * 0.12)
        sigma_boca = Line(start=LEFT, end=RIGHT, color=BLACK, stroke_width=3).scale(0.15).next_to(sigma_ojos, DOWN, buff=0.1).rotate(0.1)
        
        sigma_creature = VGroup(sigma_symbol, sigma_ojos, sigma_boca).to_edge(RIGHT, buff=3.0)

        # Globo para texto
        bubble_width = 6.0
        bubble_height = 1.2
        bubble_body = RoundedRectangle(
            corner_radius=bubble_height / 2, 
            height=bubble_height, 
            width=bubble_width, 
            color=WHITE, 
            stroke_width=3
        )
        tip_apex = bubble_body.get_bottom() + DOWN*0.4 + RIGHT*2 
        tip_base_l = bubble_body.get_bottom() + RIGHT*0.8 
        tip_base_r = bubble_body.get_bottom() + RIGHT*2.2 
        bubble_tip = Polygon(tip_base_l, tip_apex, tip_base_r, color=WHITE, stroke_width=3)
        
        final_bubble_shape = Union(bubble_body, bubble_tip)
        final_bubble_shape.set_stroke(color=WHITE, width=3)
        final_bubble_shape.set_fill(opacity=0) 

        # Texto pregunta
        question_text = Tex(r"¿Y si tengo más variables?", font_size=38, color=WHITE)
        question_text.move_to(bubble_body.get_center())

        speech_bubble = VGroup(final_bubble_shape, question_text)
        speech_bubble.next_to(sigma_creature, UP + LEFT, buff=0.2).shift(RIGHT * 1.8)

        self.play(
            FadeIn(pi_creature, shift=RIGHT), 
            FadeIn(sigma_creature, shift=LEFT), 
            run_time=1.0
        )
        self.wait(0.2) 

        self.play(sigma_creature.animate.rotate(0.05 * PI), run_time=0.3)
        self.play(sigma_creature.animate.rotate(-0.05 * PI), run_time=0.3)

        self.play(
            Write(speech_bubble),
            pi_ojos.animate.scale(1.15),
            run_time=1.0
        )
        
        ojos_sigma = sigma_creature[1]
        self.play(ojos_sigma.animate.scale_to_fit_height(0.02), run_time=0.15)
        self.play(ojos_sigma.animate.scale_to_fit_height(0.26), run_time=0.15)
        self.wait(1.4)

        variables_formula = MathTex(r"X = (x_1, x_2, \dots, x_n)", font_size=48, color=WHITE)
        variables_formula.move_to(DOWN * 2)

        self.play(Write(variables_formula), run_time=1.0)
        self.wait(1.5)
        
        self.play(
            *[FadeOut(pi_creature), 
            FadeOut(sigma_creature), 
            FadeOut(speech_bubble),
            FadeOut(variables_formula)],
            run_time=0.5
        )
    
        # 9) Grafica 3D
        self.move_camera(phi=75 * DEGREES, theta=-45 * DEGREES)

        axes3d = ThreeDAxes(
            x_range=[0, 5, 1], y_range=[0, 5, 1], z_range=[0, 5, 1],
            x_length=5, y_length=5, z_length=4,
            axis_config={"color": GREY, "include_tip": True, "font_size": 20},
        )
      
        lab_x1 = MathTex("x_1").scale(0.8)
        lab_x2 = MathTex("x_2").scale(0.8)
        lab_y  = MathTex("Y").scale(0.8)

        lab_x1.move_to(axes3d.c2p(5.5, 0, 0))  
        lab_x2.move_to(axes3d.c2p(0, 5.5, 0))  
        lab_y.move_to(axes3d.c2p(0, 0, 4.5))   
        lab_y.shift(LEFT * 0.9) 

        for label in [lab_x1, lab_x2, lab_y]:        
            label.rotate(90 * DEGREES, axis=RIGHT)
            label.rotate(45 * DEGREES, axis=OUT)

        labels3d = VGroup(lab_x1, lab_x2, lab_y)

        data_points_3d = [
            (1, 1, 1.8), (2, 1, 2.3), (1, 3, 2.6), (3, 2, 3.1), (2, 4, 3.5), 
            (4, 1, 3.2), (3.5, 3.5, 4.1), (4, 2, 3.8), (1.5, 2.5, 2.7)
        ]
        dots3d = VGroup()
        for x1, x2, y in data_points_3d:
            dots3d.add(Dot3D(axes3d.c2p(x1, x2, y), color=BLUE, radius=0.08))

        w1_val, w2_val, b_val = 0.5, 0.4, 1.0
        plane = Surface(
            lambda u, v: axes3d.c2p(u, v, w1_val*u + w2_val*v + b_val),
            u_range=[0, 5], v_range=[0, 5], resolution=(12, 12),
            fill_color=YELLOW, fill_opacity=0.3, stroke_color=YELLOW_E, stroke_width=1
        )

        plot_group = VGroup(axes3d, labels3d, dots3d, plane)
        plot_group.shift(LEFT * 5 + IN * 2)

        self.play(Create(axes3d), Write(labels3d), run_time=0.8)
        self.play(FadeIn(dots3d, lag_ratio=0.1), run_time=0.7)
        
        plane_formula_b = MathTex(r"Y = w_1 x_1 + w_2 x_2 +", r"b", color=YELLOW, font_size=40)
        plane_formula_b.to_corner(UL).shift(RIGHT*1.0 + DOWN*0.5)
        plane_formula_Final = MathTex(r"Y = w_1 x_1 + w_2 x_2 +", r"w_0", color=YELLOW, font_size=40)
        plane_formula_Final.move_to(plane_formula_b, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(plane_formula_b, plane_formula_Final)
        self.remove(plane_formula_Final) 

        self.play(
            Create(plane),
            Write(plane_formula_b),
            run_time=1.5
        )
        self.wait(0.5)

        self.play(
            ReplacementTransform(plane_formula_b, plane_formula_Final),
            run_time=0.5
        )
        plane_formula = plane_formula_Final 
        self.wait(3)  
             
        # 10) Generalización Regresión Lineal
        title_n = Tex(r"Generalizando a $n$ variables:", font_size=36, color=BLUE)
        algebraic_n = MathTex(
            r"Y = w_0 \cdot 1 + w_1 x_1 + \dots + w_n x_n",
            font_size=38,
            color=YELLOW
        )
        
        algebraic_n[0][2:4].set_color(ORANGE) # w_0
        algebraic_n[0][5].set_color(ORANGE)   # 1

        matrix_n = MathTex(
            r"Y = \mathbf{W}^T \mathbf{X}",
            font_size=48,
            color=YELLOW
        )

        vector_def = MathTex(
            r"\text{donde } \mathbf{X} = [1, x_1, \dots, x_n]",
            font_size=30,
            color=WHITE
        )
        vector_def[0][8].set_color(ORANGE) 

        error_n_formula = MathTex(
            r"Error = \frac{1}{n} \sum (y_i - \hat{y}_i)^2",
            font_size=36,
            color=RED_B
        )

        final_group = VGroup(title_n, algebraic_n, matrix_n, vector_def, error_n_formula)
        final_group.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        final_group.to_corner(UR).shift(DOWN * 0.8 + LEFT * 0.5)

        self.add_fixed_in_frame_mobjects(final_group)
        self.remove(final_group) 

        self.play(Write(title_n), run_time=0.5) # Rápido
        self.play(
            ReplacementTransform(plane_formula, algebraic_n), 
            run_time=1.0
        )
        
        self.wait(0.5)

        self.play(TransformFromCopy(algebraic_n, matrix_n), run_time=1.0)
        self.play(Write(vector_def), run_time=1.0)
        self.wait(0.5)
        
        self.play(Write(error_n_formula), run_time=1.5)
        self.wait(4)

        # 11) Sigma
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.5
        )

        self.move_camera(phi=0, theta=-90 * DEGREES)

        def crear_ojos(pupila_direction=ORIGIN, radio_pupila=0.05):
            ojo_blanco = Circle(radius=0.13, color=WHITE, fill_opacity=1, stroke_width=2)
            pupila = Dot(radius=radio_pupila, color=BLACK)
            pupila.shift(pupila_direction * 0.06)
            return VGroup(ojo_blanco, pupila)

        sigma_symbol = MathTex(r"\Sigma", font_size=180, color=BLUE)
    
        sigma_ojo_l = crear_ojos(LEFT + UP)
        sigma_ojo_r = crear_ojos(LEFT + UP)
        sigma_ojos = VGroup(sigma_ojo_l, sigma_ojo_r).arrange(RIGHT, buff=0.05)
        sigma_ojos.move_to(sigma_symbol.get_top() + RIGHT * 0.18 + DOWN * 0.12)
        
        sigma_boca = Line(start=LEFT, end=RIGHT, color=BLACK, stroke_width=3).scale(0.15)
        sigma_boca.next_to(sigma_ojos, DOWN, buff=0.1).rotate(-0.15)
        
        sigma_creature = VGroup(sigma_symbol, sigma_ojos, sigma_boca)
        sigma_creature.to_corner(DR, buff=1.0).shift(UP * 1.8 + RIGHT*0.6)

        # Globo de texto
        bubble_width = 9
        bubble_height = 1.2
        bubble_body = RoundedRectangle(corner_radius=bubble_height/2, height=bubble_height, width=bubble_width, color=WHITE, stroke_width=3)
        tip_apex = bubble_body.get_bottom() + DOWN*0.4 + RIGHT*2 
        tip_base_l = bubble_body.get_bottom() + RIGHT*0.8 
        tip_base_r = bubble_body.get_bottom() + RIGHT*2.2 
        bubble_tip = Polygon(tip_base_l, tip_apex, tip_base_r, color=WHITE, stroke_width=3)
        final_bubble_shape = Union(bubble_body, bubble_tip).set_stroke(color=WHITE, width=3).set_fill(opacity=0) 

        question_text = Tex(r"¿Y si los datos no siguen una distribución lineal?", font_size=38, color=WHITE)
        question_text.move_to(bubble_body.get_center())

        speech_bubble = VGroup(final_bubble_shape, question_text)
        speech_bubble.next_to(sigma_creature, UP + LEFT, buff=0.1)
        speech_bubble.shift(RIGHT * 1.5)

        self.play(FadeIn(sigma_creature, shift=LEFT), run_time=0.5)
        self.play(Write(speech_bubble))
        self.wait(1)


        axes_fail = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            x_length=6.5,  
            y_length=4.5,
            axis_config={"color": GREY, "include_tip": False, "font_size": 24},
        ).add_coordinates(font_size=20)
        
        axes_fail.to_edge(LEFT, buff=1.0).shift(DOWN * 1.3)
        labels_fail = axes_fail.get_axis_labels(x_label="X", y_label="Y")

        x_u = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        y_u = [6.0, 4.0, 3.2, 2.0, 2.0, 2.2, 3.0, 4.4, 5.7]

        dots_u = VGroup()
        for x, y in zip(x_u, y_u):
            dots_u.add(Dot(axes_fail.c2p(x, y), color=BLUE))

        self.play(
            Create(axes_fail), 
            Write(labels_fail),
            FadeIn(dots_u, lag_ratio=0.1),
            run_time=1.0
        )
        
        y_pred_val = 3.6
        bad_line = axes_fail.plot(lambda x: y_pred_val, color=YELLOW)
        bad_formula = MathTex(r"Y = wX + b", color=YELLOW, font_size=30)
        bad_formula.next_to(bad_line, UP, buff=0.1)

        self.play(Create(bad_line), Write(bad_formula), run_time=0.5)

        errors_u = VGroup()
        for x, y in zip(x_u, y_u):
            start = axes_fail.c2p(x, y)
            end = axes_fail.c2p(x, y_pred_val)
            errors_u.add(Line(start, end, color=RED, stroke_width=3))

        fail_text = Text("¡El error es demasiado grande!", color=RED, font_size=42)
        fail_text.to_edge(UP, buff=1.0).shift(LEFT * 1.0)

        self.play(
            bad_line.animate.set_color(RED),
            bad_formula.animate.set_color(RED),
            Wiggle(bad_line, scale_value=1.2, rotation_angle=0.03 * TAU),
            Create(errors_u),
            Write(fail_text),
            run_time=1.0 
        )
        self.wait(0.5)

        # 13) Regresión no lineal
        new_title = Text("Regresión No Lineal", font_size=36).to_edge(UP)
        graph_group = VGroup(axes_fail, labels_fail, dots_u, bad_line, bad_formula)

        self.play(
            FadeOut(sigma_creature),
            FadeOut(speech_bubble),
            FadeOut(fail_text),
            FadeOut(errors_u),
            graph_group.animate.move_to(ORIGIN + DOWN * 0.5),
            Write(new_title),
            run_time=1.0
        )
        
        poly_formula = MathTex(
            r"y = w_0 + w_1 x + w_2 x^2", 
            color=GREEN, 
            font_size=38
        )
        
        fit_curve = axes_fail.plot(lambda x: 0.25 * (x - 5)**2 + 2, color=GREEN, stroke_width=4)

        self.play(
            Transform(bad_line, fit_curve),
            ReplacementTransform(bad_formula, poly_formula),
            run_time=1.5
        )

        w0_val = MathTex(r"w_0 \approx 8.25", color=WHITE, font_size=30)
        w1_val = MathTex(r"w_1 \approx -2.50", color=WHITE, font_size=30)
        w2_val = MathTex(r"w_2 \approx 0.25", color=WHITE, font_size=30)

        values_group = VGroup(w0_val, w1_val, w2_val).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        values_group.next_to(poly_formula, DOWN, buff=0.3)

        self.play(
            Write(values_group),
            Indicate(poly_formula, color=GREEN_B, scale_factor=1.1),
            run_time=1.0
        )       
        self.wait(2.5)

        # 14) Superficie
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1
        )

        self.move_camera(phi=70 * DEGREES, theta=-45 * DEGREES)

        poly_formula_slide = MathTex(
            r"h(x_i) = w_0 + w_1 x_i + w_2 x_i^2 + \dots",
            font_size=42,
            color=GREEN
        )
        poly_formula_slide.to_edge(DOWN).shift(UP * 0.5)
        self.add_fixed_in_frame_mobjects(poly_formula_slide)
        self.remove(poly_formula_slide)

        axes_surface = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-1, 5, 1],
            x_length=6, y_length=6, z_length=4,
            axis_config={"color": GREY, "include_tip": True, "font_size": 20},
        )

        x_label = MathTex("x_1").scale(0.9)
        y_label = MathTex("x_2").scale(0.9)
        z_label = MathTex("h(x)").scale(0.9)

        x_label.move_to(axes_surface.c2p(3.5, 0, 0))  
        y_label.move_to(axes_surface.c2p(0, 3.5, 0))  
        z_label.move_to(axes_surface.c2p(0, 0, 5.5)) 

        for label in [x_label, y_label, z_label]:
            label.rotate(90 * DEGREES, axis=RIGHT) 
            label.rotate(45 * DEGREES, axis=OUT)   

        z_label.shift(LEFT * 0.2)
        labels_surf = VGroup(x_label, y_label, z_label)

        def param_surface(u, v):
            x = u
            y = v
            z = 3 * np.exp(-(x**2 + y**2) / 4) 
            return axes_surface.c2p(x, y, z)

        surface = Surface(
            param_surface,
            u_range=[-3, 3], v_range=[-3, 3], resolution=(16, 16), 
            fill_color=BLUE_D, fill_opacity=0.5,
            stroke_color=WHITE, stroke_width=0.5,
            checkerboard_colors=[BLUE_D, BLUE_E],
        )

        dots_surface = VGroup()
        np.random.seed(42)
        for _ in range(15): 
            u = np.random.uniform(-2.5, 2.5)
            v = np.random.uniform(-2.5, 2.5)
            z_base = 3 * np.exp(-(u**2 + v**2) / 4)
            z_noise = np.random.uniform(-0.3, 0.3)
            dot = Dot3D(axes_surface.c2p(u, v, z_base + z_noise), color=YELLOW, radius=0.08)
            dots_surface.add(dot)

        graph_group = VGroup(axes_surface, labels_surf, surface, dots_surface)
        graph_group.shift(DOWN * 1.5 + RIGHT * 0.8)

        self.play(
            Create(axes_surface), 
            Write(labels_surf),
            Write(poly_formula_slide),
            run_time=1.5
        )

        self.play(FadeIn(dots_surface, lag_ratio=0.1), run_time=1.0)
        self.play(Create(surface), run_time=2.0)
        self.wait(3)

        # 15) Generalización matricial
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            FadeOut(poly_formula_slide), 
            run_time=1.0
        )
        
        self.move_camera(phi=0, theta=-90 * DEGREES) 
        title_n = Tex(r"Generalizando (Notación Matricial):", font_size=36, color=BLUE)

        sum_formula = MathTex(
            r"h(x_i) = \sum_{j=0}^{p} w_j x_i^j",
            font_size=44,
            color=YELLOW
        )

        matrix_n = MathTex(
            r"h(\mathbf{X}) = \mathbf{X}\mathbf{W}^T",
            font_size=56, 
            color=YELLOW
        )

        vector_def = MathTex(
            r"\text{donde } \mathbf{X} = [1, x, x^2, \dots, x^p]",
            font_size=32,
            color=WHITE
        )

        error_slide_formula = MathTex(
            r"\text{Error} = \frac{\sum(y_i - \hat{y}_i)^2}{n}",
            font_size=40,
            color=RED_B
        )

        final_group = VGroup(title_n, sum_formula, matrix_n, vector_def, error_slide_formula)        
        final_group.arrange(DOWN, buff=0.6)
        final_group.move_to(ORIGIN) 

        self.play(Write(title_n), run_time=0.8)
        self.wait(0.2)
        
        self.play(Write(sum_formula), run_time=0.8)
        self.wait(0.3)

        self.play(TransformFromCopy(sum_formula, matrix_n))
        self.wait(0.5)

        self.play(Write(vector_def))
        self.wait(0.5)

        self.play(Write(error_slide_formula))        
        self.wait(4)

        # 16) Graficas (recapitulación)
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1.0
        )

        # grafica 1
        cam_theta = 30 
        self.move_camera(phi=75 * DEGREES, theta=cam_theta * DEGREES, zoom=0.6)

        axes_1 = Axes(x_range=[0, 5], y_range=[0, 5], x_length=4, y_length=4)
        line_1 = axes_1.plot(lambda x: 0.8 * x + 0.5, color=YELLOW)
        dots_1 = VGroup(*[Dot(axes_1.c2p(x, 0.8*x + 0.5 + np.random.uniform(-0.3, 0.3)), color=BLUE, radius=0.1) for x in range(1, 5)])
        
        plot_content_1 = VGroup(axes_1, line_1, dots_1)
        plot_content_1.rotate(90 * DEGREES, axis=RIGHT).rotate(90 * DEGREES, axis=OUT)
        
        label_1 = Text("Lineal (2D)", font_size=36, color=WHITE)
        label_1.rotate(90 * DEGREES, axis=RIGHT)
        label_1.rotate((cam_theta + 90) * DEGREES, axis=OUT)
        label_1.next_to(plot_content_1, OUT, buff=0.5)
        
        group_1 = VGroup(plot_content_1, label_1)
        group_1.move_to(LEFT * 6)

        # grafica 2
        axes_2 = ThreeDAxes(x_range=[-2, 2], y_range=[-2, 2], z_range=[-2, 2], x_length=4, y_length=4, z_length=3)
        plane_2 = Surface(
            lambda u, v: axes_2.c2p(u, v, 0.5*u + 0.3*v),
            u_range=[-2, 2], v_range=[-2, 2], resolution=(8, 8),
            fill_color=BLUE, fill_opacity=0.3, stroke_width=0.5
        )
        
        label_2 = Text("Múltiple (Plano)", font_size=36, color=WHITE)
        label_2.rotate(90 * DEGREES, axis=RIGHT)
        label_2.rotate((cam_theta + 90) * DEGREES, axis=OUT)
        label_2.next_to(axes_2, OUT, buff=0.5)
        
        group_2 = VGroup(axes_2, plane_2, label_2)
        group_2.move_to(ORIGIN)

        # gráfica 3
        axes_3 = ThreeDAxes(x_range=[-2, 2], y_range=[-2, 2], z_range=[0, 4], x_length=4, y_length=4, z_length=3)
        surface_3 = Surface(
            lambda u, v: axes_3.c2p(u, v, 3 * np.exp(-(u**2 + v**2)/2)), 
            u_range=[-2, 2], v_range=[-2, 2], resolution=(12, 12),
            fill_color=TEAL, fill_opacity=0.5, checkerboard_colors=[TEAL, BLUE_E], stroke_width=0.5
        )
        
        label_3 = Text("No Lineal (Curva)", font_size=36, color=WHITE)
        label_3.rotate(90 * DEGREES, axis=RIGHT)
        label_3.rotate((cam_theta + 90) * DEGREES, axis=OUT)
        label_3.next_to(axes_3, OUT, buff=0.5)

        group_3 = VGroup(axes_3, surface_3, label_3)
        group_3.move_to(RIGHT * 6)

        self.play(
            LaggedStart(
                FadeIn(group_1, shift=UP),
                FadeIn(group_2, shift=UP),
                FadeIn(group_3, shift=UP),
                lag_ratio=0.2 
            ),
            run_time=1.5
        )

        self.begin_ambient_camera_rotation(rate=0.3) 
        self.wait(2.5)
        self.stop_ambient_camera_rotation()

        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1.0
        )        

        # 17) Frase final
        self.move_camera(phi=0, theta=-90 * DEGREES)
        quote = Tex(
            r"``Todos los ",           
            r"modelos",                # CELESTE
            r" están ", 
            r"equivocados",
            r",\\",
            r"pero algunos nos acercan más a la ",     
            r"realidad",                 # CELESTE
            r".''"                     
        )

        quote.scale(1.8).shift(UP * 0.5)

        quote[1].set_color(BLUE)  # "modelos"
        quote[3].set_color(RED)  # "equivocados"
        quote[6].set_color(BLUE)  # "útiles"


        self.play(Write(quote), run_time=3)
        self.wait(2)
        self.play(FadeOut(quote), run_time=0.5)
        self.wait(1)