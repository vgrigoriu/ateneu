from hello import normalize


def test_normalize_event_691_desription():
    response = normalize("""<p><strong>Orchestra simfonică a Filarmonicii George Enescu</strong></p>
<p>Dirijor<strong> <br/>MIKHAIL PLETNEV </strong></p>
<p>Solistă<br/><strong>IOANA CRISTINA GOICEA </strong></p>
<p>Program</p>
<p><strong>Alfred Alessandrescu<br/></strong>Amurg de toamnă</p>
<p><strong>Jean Sibelius<br/></strong>Concertul în re minor pentru vioară și orchestră, op. 47</p>
<p><strong>Aleksandr Glazunov</strong> <br/>Anotimpurile, op. 67</p>
""")
    actual = [str(element) for element in response]
    expected = [
        "<p><strong>Orchestra simfonică a Filarmonicii George Enescu</strong></p>",
        "<p>Dirijor<strong> <br/>MIKHAIL PLETNEV </strong></p>",
        "<p>Solistă<br/><strong>IOANA CRISTINA GOICEA </strong></p>",
        "<p>Program</p>",
        "<p><strong>Alfred Alessandrescu<br/></strong>Amurg de toamnă</p>",
        "<p><strong>Jean Sibelius<br/></strong>Concertul în re minor pentru vioară și orchestră, op. 47</p>",
        "<p><strong>Aleksandr Glazunov</strong> <br/>Anotimpurile, op. 67</p>",
    ]
    assert actual == expected


def test_normalize_event_693_description():
    response = normalize("""<p><strong>Orchestra simfonică a Filarmonicii George Enescu</strong></p>
<p>Dirijor <br/><strong>GABRIEL BEBEȘELEA</strong></p>
<p>Solist <br/><strong>BRUCE LIU</strong></p>
<p>Program</p>
<p><strong>George Enescu</strong><br/>Pastorale-Fantaisie</p>
<p><strong>Aleksandr Scriabin</strong><br/>Concertul în fa diez minor pentru pian și orchestră, op. 20</p>
<p><strong>Paul Dukas</strong><br/>Ucenicul vrăjitor</p>
<p><strong>Aleksandr Scriabin</strong><br/>Poemul extazului, op. 54</p>
""")
    actual = [str(element) for element in response]
    expected = [
        "<p><strong>Orchestra simfonică a Filarmonicii George Enescu</strong></p>",
        "<p>Dirijor <br/><strong>GABRIEL BEBEȘELEA</strong></p>",
        "<p>Solist <br/><strong>BRUCE LIU</strong></p>",
        "<p>Program</p>",
        "<p><strong>George Enescu</strong><br/>Pastorale-Fantaisie</p>",
        "<p><strong>Aleksandr Scriabin</strong><br/>Concertul în fa diez minor pentru pian și orchestră, op. 20</p>",
        "<p><strong>Paul Dukas</strong><br/>Ucenicul vrăjitor</p>",
        "<p><strong>Aleksandr Scriabin</strong><br/>Poemul extazului, op. 54</p>",
    ]
    assert actual == expected


def test_normalize_event_695_description():
    response = normalize("""<p><strong>Orchestra simfonică a Filarmonicii George Enescu</strong></p>
<p>Dirijor <br/><strong>KRISTJAN JÄRVI</strong></p>
<p>Solist <br/><strong>VLAD STĂNCULEASA</strong></p>
<p>Program</p>
<p><strong>Kristjan Järvi<br/></strong>Aurora</p>
<p><strong>Felix Mendelssohn<br/></strong>Concertul în mi minor pentru vioară şi orchestră, op. 64</p>
<p><strong>Jean Sibelius<br/></strong>Simfonia nr. 2, în re major, op. 43</p>
""")
    actual = [str(element) for element in response]
    expected = [
        "<p><strong>Orchestra simfonică a Filarmonicii George Enescu</strong></p>",
        "<p>Dirijor <br/><strong>KRISTJAN JÄRVI</strong></p>",
        "<p>Solist <br/><strong>VLAD STĂNCULEASA</strong></p>",
        "<p>Program</p>",
        "<p><strong>Kristjan Järvi<br/></strong>Aurora</p>",
        "<p><strong>Felix Mendelssohn<br/></strong>Concertul în mi minor pentru vioară şi orchestră, op. 64</p>",
        "<p><strong>Jean Sibelius<br/></strong>Simfonia nr. 2, în re major, op. 43</p>",
    ]
    assert actual == expected


def test_normalize_event_697_description():
    response = normalize("""<p><strong>Orchestra Simfonică şi Corul Filarmonicii George Enescu</strong></p>
<p>Dirijor <br/><strong>ARNAUD ARBET</strong></p>
<p>Solist <br/><strong>DAVID KADOUCH</strong></p>
<p>Program</p>
<p><strong>Gabriel Fauré<br/></strong>Pavană, op. 50</p>
<p><strong>Camille Saint-Saëns</strong><br/>Concertul nr. 1, în re major, pentru pian și orchestră, op. 17</p>
<p><strong>Claude Debussy<br/></strong>Nocturne<span> </span><span> </span></p>
<p><strong>Maurice Ravel<br/></strong>Boléro</p>
<p>Dirijorul corului<br/><strong>IOSIF ION PRUNNER</strong></p>
<p><strong> </strong></p>""")
    actual = [str(element) for element in response]
    expected = [
        "<p><strong>Orchestra Simfonică şi Corul Filarmonicii George Enescu</strong></p>",
        "<p>Dirijor <br/><strong>ARNAUD ARBET</strong></p>",
        "<p>Solist <br/><strong>DAVID KADOUCH</strong></p>",
        "<p>Program</p>",
        "<p><strong>Gabriel Fauré<br/></strong>Pavană, op. 50</p>",
        "<p><strong>Camille Saint-Saëns</strong><br/>Concertul nr. 1, în re major, pentru pian și orchestră, op. 17</p>",
        "<p><strong>Claude Debussy<br/></strong>Nocturne</p>",
        "<p><strong>Maurice Ravel<br/></strong>Boléro</p>",
        "<p>Dirijorul corului<br/><strong>IOSIF ION PRUNNER</strong></p>",
    ]
    assert actual == expected
