def test_func(c_string):
    # c_string = request.session.get('cmode')
    # print request.session.session_key
    # print c_string
    outhead1string = '<hr /><span class="boldlarge">Calculation Mode: ' + str(c_string) + '</span>'
    return  outhead1string