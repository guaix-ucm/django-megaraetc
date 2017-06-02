def bokehplot1(sourcet,
               x, y, ysky,
               x3, y3, z3,
               vph_minval, vph_maxval,
               label1, label2, label3,
               x2, y2, x2b, y2b,
               x2c, y2c, x2d, y2d,
               label2a, label2b, label2c,
               fluxt, lambc):
    from bokeh.plotting import figure
    from bokeh.resources import CDN
    from bokeh.embed import components
    from bokeh.layouts import column
    from bokeh.models import Span
    from bokeh.models import Legend, Label, Range1d


    # x[0::10]    # too much datapoints, extract every 10
    # y[0::10]    # do the same here
    p1 = figure(plot_height=400, active_scroll="wheel_zoom", toolbar_location="above", webgl=True)
    inputsource = p1.line(x, y, color='blue')
    # p1.line(x, ysky, color='cyan')
    vlineg = Span(location=float(x3), dimension='height', line_color='green', line_width=1, line_dash='dashed')
    vlinemin = Span(location=float(vph_minval), dimension='height', line_color='red', line_width=1, line_dash='dashed')
    vlinemax = Span(location=float(vph_maxval), dimension='height', line_color='red', line_width=1, line_dash='dashed')
    vlinelambc = Span(location=float(lambc), dimension='height', line_color='orange', line_width=1, line_dash='dashed')
    p1.renderers.extend([vlineg, vlinemin, vlinemax, vlinelambc])

    # Change according to input source type (P or E)
    if sourcet=='P' or sourcet=='Point':
        p1.yaxis.axis_label = "Flux (erg/s/cm2/Angstrom) per seeing area"
    else:
        p1.yaxis.axis_label = "Flux (erg/s/cm2/Angstrom/arcsec2)"

    p1.xaxis.axis_label = "Wavelength (Angstrom)"
    p1.x_range = Range1d(vph_minval-100, vph_maxval+100)

    if label1=='Uniform':
        p1.y_range = Range1d(0,2*max(y))
    if fluxt == 'L':
        legend1 = Legend(items=[
        ("VPH min max", [p1.line(0, 0, line_dash='dashed', line_width=1, color='red')]),
        ("VPH lambda_c" , [p1.line(0, 0, line_dash='dashed', line_width=1, color='orange')]),
        ("input line" , [p1.line(0, 0, line_dash='dashed', line_width=1, color='green')]),
        ('', []),
        ('Source: ' + str(label1), [inputsource]),
        ('Cont. mag: ' + str('%.2f' % label2), []),
        ('Cont. band: ' + str(label3), []),
        ],
        location=(1, 45),
        )
    else:
        legend1 = Legend(items=[
        ("VPH min max", [p1.line(0, 0, line_dash='dashed', line_width=1, line_color='red')]),
        ("VPH lambda_c" , [p1.line(0, 0, line_dash='dashed', line_width=1, line_color='orange')]),
        ('', []),
        ('Source: ' + str(label1), [inputsource]),
        ('Cont. mag: ' + str(label2), []),
        ('Cont. band: ' + str(label3), []),
        ],
        location=(1, 45),
        )

    p1.legend.border_line_alpha = 0.5
    p1.add_layout(legend1, 'right') # to plot outside fo plot


    p2 = figure(plot_height=400,
                x_range=p1.x_range, active_scroll="wheel_zoom", toolbar_location="above", webgl=True)
    p2.multi_line([x2, x2b, x2c, x2d], [y2, y2b, y2c,y2d],
                  color=['red', 'red', 'blue','blue'], line_dash='solid', line_width=[1,3,1,3])
    # p2.line(x2b,y2b, color='red', line_dash='dashed')
    p2.renderers.extend([vlineg, vlinemin, vlinemax, vlinelambc])
    p2.yaxis.axis_label = "SNR per voxel"
    p2.xaxis.axis_label = "Wavelength (Angstrom)"

    if fluxt=='L':
        legend2 = Legend(items=[
            ("per-fr. c fib.", [p2.line(0, 0, line_width=1, color='red')]),
            ("all-fr. c fib." , [p2.line(0, 0, line_width=3, color='red')]),
            ("per-fr. c+r1 fibs." , [p2.line(0, 0, line_width=1, color='blue')]),
            ("all-fr. c+r1 fibs.", [p2.line(0, 0, line_width=3, color='blue')]),
            ("", []),
            ("Source: " + str(label2a), []),
            ("VPH: " + str(label2b), []),
            ("Cont. band: " + str(label2c), []),
            ],
            location=(1, 45),
            )
    else:
        legend2 = Legend(items=[
            ("per-fr. 1 fib.", [p2.line(0, 0, line_width=1, color='red')]),
            ("all-fr. 1 fib." , [p2.line(0, 0, line_width=3, color='red')]),
            ("per-fr. all fibs." , [p2.line(0, 0, line_width=1, color='blue')]),
            ("all-fr. all fibs.", [p2.line(0, 0, line_width=3, color='blue')]),
            ("", []),
            ("Source: " + str(label2a), []),
            ("VPH: " + str(label2b), []),
            ("Cont. band: " + str(label2c), []),
            ],
            location=(1, 45),
            )

    p2.legend.border_line_alpha = 0.5
    p2.add_layout(legend2, 'right')

    # legend3 = Legend(items=[
    #     ("Source:"+str(label1), [p2.circle(0, 0, line_width=0, fill_alpha=0)]),
    #     ],
    #     location=(20, -30),
    #     )
    # citation2 = Label(x=450, y=100, x_units='screen', y_units='screen',
    #              text='Source: '+str(label2a)+'<BR />VPH: '+
    #                   str(label2b)+'<BR />Cont. band: '+
    #                   str(label2c),
    #             render_mode='css',
    #              border_line_color='black', border_line_alpha=1.0,
    #              background_fill_color='white', background_fill_alpha=1.0
    #                  )
    # p2.add_layout(citation2)

    # layout plots in a column
    allplots = column(p1, p2)

    # ouptut js script and html <div>
    thescript, thediv = components(allplots, CDN)

    return thescript, thediv