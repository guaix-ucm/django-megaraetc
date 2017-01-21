def bokehplot1(x, y,
               x3, y3, z3,
               vph_minval, vph_maxval,
               label1, label2, label3,
               x2, y2, x2b, y2b,
               x2c, y2c, x2d, y2d,
               label2a, label2b, label2c,
               fluxt):
    from bokeh.plotting import figure
    from bokeh.resources import CDN
    from bokeh.embed import components
    from bokeh.layouts import column
    from bokeh.models import Span
    from bokeh.models import Legend, Label, Range1d

    # x[0::10]    # too much datapoints, extract every 10
    # y[0::10]    # do the same here
    p1 = figure(plot_height=400)
    p1.line(x, y, color='blue')
    vlineg = Span(location=float(x3), dimension='height', line_color='green', line_width=1, line_dash='dashed')
    vlinemin = Span(location=float(vph_minval), dimension='height', line_color='red', line_width=1, line_dash='dashed')
    vlinemax = Span(location=float(vph_maxval), dimension='height', line_color='red', line_width=1, line_dash='dashed')
    p1.renderers.extend([vlineg, vlinemin, vlinemax])
    p1.yaxis.axis_label = "Flux (erg/s/cm2/Angstrom)"
    p1.xaxis.axis_label = "Wavelength (Angstrom)"
    p1.x_range = Range1d(4000, max(x))
    citation1 = Label(x=450, y=100,
                      x_units='screen', y_units='screen',
                      text='Source: '+str(label1)+
                           '<BR />Cont. mag: '+str(label2)+
                           '<BR />Cont. band: '+str(label3),
                      render_mode='css',
                      border_line_color='black', border_line_alpha=1.0,
                      background_fill_color='white', background_fill_alpha=1.0
                      )
    p1.add_layout(citation1)


    p2 = figure(plot_height=400,
                x_range=p1.x_range)
    p2.multi_line([x2, x2b, x2c, x2d], [y2, y2b, y2c,y2d],
                  color=['red', 'red', 'blue','blue'], line_dash='solid', line_width=[1,3,1,3])
    # p2.line(x2b,y2b, color='red', line_dash='dashed')
    p2.renderers.extend([vlineg, vlinemin, vlinemax])
    p2.yaxis.axis_label = "SNR per voxel"
    p2.xaxis.axis_label = "Wavelength (Angstrom)"

    if fluxt=='L':
        legend2 = Legend(items=[
            ("per frame c fiber", [p2.line(line_width=1, color='red')]),
            ("all frames c fiber" , [p2.line(line_width=3, color='red')]),
            ("per frame c+r1 fibers" , [p2.line(line_width=1, color='blue')]),
            ("all frames c+r1 fibers", [p2.line(line_width=3, color='blue')]),
            ],
            location=(20, -30),
            )
    else:
        legend2 = Legend(items=[
            ("per frame 1 fiber", [p2.line(line_width=1, color='red')]),
            ("all frames 1 fiber" , [p2.line(line_width=3, color='red')]),
            ("per frame all fibers" , [p2.line(line_width=1, color='blue')]),
            ("all frames all fibers", [p2.line(line_width=3, color='blue')]),
            ],
            location=(20, -30),
            )

    p2.legend.border_line_alpha = 0.5
    p2.add_layout(legend2, 'right')

    # legend3 = Legend(items=[
    #     ("Source:"+str(label1), [p2.circle(line_width=0, fill_alpha=0)]),
    #     ],
    #     location=(20, -30),
    #     )
    citation2 = Label(x=450, y=100, x_units='screen', y_units='screen',
                 text='Source: '+str(label2a)+'<BR />VPH: '+
                      str(label2b)+'<BR />Cont. band: '+
                      str(label2c),
                render_mode='css',
                 border_line_color='black', border_line_alpha=1.0,
                 background_fill_color='white', background_fill_alpha=1.0
                     )
    p2.add_layout(citation2)

    # layout plots in a column
    allplots = column(p1, p2)

    # ouptut js script and html <div>
    thescript, thediv = components(allplots, CDN)

    return thescript, thediv