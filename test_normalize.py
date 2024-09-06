from hello import normalize


def test_normalize_event_691_desription():
    response = normalize(
        """<p><strong>Orchestra simfonică a Filarmonicii George Enescu</strong></p><p>Dirijor<strong> <br />MIKHAIL PLETNEV </strong></p><p>Solistă<br /><strong>IOANA CRISTINA GOICEA </strong></p><p>Program</p><p><strong>Alfred Alessandrescu<br /></strong>Amurg de toamnă</p><p><strong>Jean Sibelius<br /></strong>Concertul &icirc;n re minor pentru vioară și orchestră, op. 47</p><p><strong>Aleksandr Glazunov</strong> <br />Anotimpurile, op. 67</p>"""
    )
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
    response = normalize(
        """<p><strong>Orchestra simfonică a Filarmonicii George Enescu</strong></p><p>Dirijor <br /><strong>GABRIEL BEBEȘELEA</strong></p><p>Solist <br /><strong>BRUCE LIU</strong></p><p>Program</p><p><strong>George Enescu</strong><br />Pastorale-Fantaisie</p><p><strong>Aleksandr Scriabin</strong><br />Concertul &icirc;n fa diez minor pentru pian și orchestră, op. 20</p><p><strong>Paul Dukas</strong><br />Ucenicul vrăjitor</p><p><strong>Aleksandr Scriabin</strong><br />Poemul extazului, op. 54</p>"""
    )
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
    response = normalize(
        """<p><strong>Orchestra simfonică a Filarmonicii George Enescu</strong></p><p>Dirijor <br /><strong>KRISTJAN J&Auml;RVI</strong></p><p>Solist <br /><strong>VLAD STĂNCULEASA</strong></p><p>Program</p><p><strong>Kristjan J&auml;rvi<br /></strong>Aurora</p><p><strong>Felix Mendelssohn<br /></strong>Concertul &icirc;n mi minor pentru vioară şi orchestră, op. 64</p><p><strong>Jean Sibelius<br /></strong>Simfonia nr. 2, &icirc;n re major, op. 43</p>"""
    )
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
    response = normalize(
        """<p><strong>Orchestra Simfonică şi Corul Filarmonicii George Enescu</strong></p><p>Dirijor <br /><strong>ARNAUD ARBET</strong></p><p>Solist <br /><strong>DAVID KADOUCH</strong></p><p>Program</p><p><strong>Gabriel Faur&eacute;<br /></strong>Pavană, op. 50</p><p><strong>Camille Saint-Sa&euml;ns</strong><br />Concertul nr. 1, &icirc;n re major, pentru pian și orchestră, op. 17</p><p><strong>Claude Debussy<br /></strong>Nocturne<span> </span><span> </span></p><p><strong>Maurice Ravel<br /></strong>Bol&eacute;ro</p><p>Dirijorul corului<br /><strong>IOSIF ION PRUNNER</strong></p><p><strong> </strong></p>"""
    )
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


def test_normalize_event_729_description():
    response = normalize(
        """<p><strong>Orchestra Filarmonicii George Enescu</strong></p><p>Dirijor <br /><strong>ROBERTO FOR&Eacute;S-VESES</strong></p><p>Solist <br /><strong>ALEXANDRE THARAUD </strong></p><div>Program</div><div></div><div><strong>Joseph Haydn</strong><br />Simfonia nr. 85, &icirc;n si bemol major, &ldquo;Regina&rdquo;</div><div></div><div><span><strong>Ludwig van Beethoven<br /></strong>Concertul nr. 3, &icirc;n do minor, pentru pian și orchestră, op. 37 </span></div><div><span></span></div><div><span><strong>Robert Schumann<br /></strong>Simfonia nr. 4, &icirc;n re minor, op. 120 </span></div>"""
    )
    actual = [str(element) for element in response]
    expected = [
        "<p><strong>Orchestra Filarmonicii George Enescu</strong></p>",
        "<p>Dirijor <br/><strong>ROBERTO FORÉS-VESES</strong></p>",
        "<p>Solist <br/><strong>ALEXANDRE THARAUD </strong></p>",
        "<p>Program</p>",
        "<p><strong>Joseph Haydn</strong><br/>Simfonia nr. 85, în si bemol major, “Regina”</p>",
        "<p><strong>Ludwig van Beethoven<br/></strong>Concertul nr. 3, în do minor, pentru pian și orchestră, op. 37 </p>",
        "<p><strong>Robert Schumann<br/></strong>Simfonia nr. 4, în re minor, op. 120 </p>",
    ]
    assert actual == expected


def test_normalize_event_731_description():
    response = normalize(
        "<p><strong>Orchestra Filarmonicii George Enescu</strong></p><div><div><p>Dirijor <br /><strong>CHARLES DUTOIT</strong></p><p>Solistă <br /><strong>IOANA CRISTINA GOICEA </strong></p><p>Program</p><p><strong>Igor Stravinski</strong><br />Suita Pasărea de foc (1919)</p><p><strong>Serghei Prokofiev</strong><br />Concertul nr. 2, &icirc;n sol minor, pentru vioară și orchestră, op. 63</p><p><strong>Antonin Dvorak</strong><br />Simfonia nr. 9, &icirc;n mi minor, &ldquo;Din lumea nouă&rdquo;, op. 95</p><span> </span></div><span> </span></div>"
    )
    actual = [str(element) for element in response]
    expected = [
        "<p><strong>Orchestra Filarmonicii George Enescu</strong></p>",
        "<p>Dirijor <br/><strong>CHARLES DUTOIT</strong></p>",
        "<p>Solistă <br/><strong>IOANA CRISTINA GOICEA </strong></p>",
        "<p>Program</p>",
        "<p><strong>Igor Stravinski</strong><br/>Suita Pasărea de foc (1919)</p>",
        "<p><strong>Serghei Prokofiev</strong><br/>Concertul nr. 2, în sol minor, pentru vioară și orchestră, op. 63</p>",
        "<p><strong>Antonin Dvorak</strong><br/>Simfonia nr. 9, în mi minor, “Din lumea nouă”, op. 95</p>",
    ]
    assert actual == expected

def test_normalize_event_767_description():
    response = normalize("<p><tkfmedia data-tkf-mediatype=\"image\" data-tkf-id=\"66d9a08c29c82220e82d4555\" data-tkf-style=\"align:left;width:256px\" data-tkf-featured=\"true\"></tkfmedia></p><p><strong>Moștenitorii Rom&acirc;niei muzicale</strong> - un proiect Radio Rom&acirc;nia Muzical și Rotary Club Pipera</p><p>Recital extraordinar de chitară</p><p><strong>DRAGOȘ ILIE</strong></p><p>Program</p><p><strong>B&eacute;la Bart&oacute;k</strong></p><p>Sonatina (ar. Kanengiser)</p><p><strong>George Enescu</strong></p><p>Lăutarul, din Suita Impresii din copilărie (trans. Ilie)</p><p><strong>Wenzeslaus Thomas </strong><strong>Matiegka</strong></p><p>Grande Sonate nr. 1</p><p>Sonata &icirc;n si minor, op. 23 (după Haydn)</p><p><strong>Tōru Takemitsu</strong></p><p>Equinox</p><p><strong>Leo Brouwer</strong></p><p>Hika</p><p><strong>Manuel de Falla</strong></p><p>Homenaje pour Le tombeau de Claude Debussy</p><p><strong>Joaqu&iacute;n Rodrigo</strong></p><p>Invocaci&oacute;n y danza</p><p>Homenaje a Manuel de Falla</p>")
    actual = [str(element) for element in response]
    expected = [
        "<p><strong>Moștenitorii României muzicale</strong> - un proiect Radio România Muzical și Rotary Club Pipera</p>",
        "<p>Recital extraordinar de chitară</p>",
        "<p><strong>DRAGOȘ ILIE</strong></p>",
        "<p>Program</p>",
        "<p><strong>Béla Bartók</strong></p>",
        "<p>Sonatina (ar. Kanengiser)</p>",
        "<p><strong>George Enescu</strong></p>",
        "<p>Lăutarul, din Suita Impresii din copilărie (trans. Ilie)</p>",
        "<p><strong>Wenzeslaus Thomas </strong><strong>Matiegka</strong></p>",
        "<p>Grande Sonate nr. 1</p>",
        "<p>Sonata în si minor, op. 23 (după Haydn)</p>",
        "<p><strong>Tōru Takemitsu</strong></p>",
        "<p>Equinox</p>",
        "<p><strong>Leo Brouwer</strong></p>",
        "<p>Hika</p>",
        "<p><strong>Manuel de Falla</strong></p>",
        "<p>Homenaje pour Le tombeau de Claude Debussy</p>",
        "<p><strong>Joaquín Rodrigo</strong></p>",
        "<p>Invocación y danza</p>",
        "<p>Homenaje a Manuel de Falla</p>",
    ]
    assert actual == expected