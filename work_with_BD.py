import patoolib
from lxml import etree
from datetime import datetime
from dateutil import parser
import requests
import os.path
import BD 

def writing_to_BD(session):
    url = 'http://programtv.ru/xmltv.xml.gz'
    response = requests.get(url)

    xml_gz = open(os.path.dirname(os.path.realpath(__file__)) +'\\xmltv.xml.gz', 'wb')
    xml_gz.write(response.content)
    xml_gz.close()

    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    patoolib.extract_archive(os.path.dirname(os.path.realpath(__file__)) +'\\xmltv.xml.gz', outdir=os.path.dirname(os.path.realpath(__file__)))
    with open("xmltv.xml", encoding = 'utf-8') as fobj:
        xml = fobj.read().encode('utf-8')
    
    root = etree.fromstring(xml)

    for elem in root:
        if elem.tag == "channel":
            res_channel = session.query(BD.Channel.name).filter(BD.Channel.id_channel == elem.get('id'))
            count = 0
            for ch in res_channel:
                count += 1 

            if count == 0:
                table_channel = BD.Channel(id_channel = elem.get('id'), name = elem[1].text)
                session.add(table_channel)
                #session.commit()

        if  elem.tag == "programme":
            res_id_telecast = session.query(BD.Telecast.id).filter(BD.Telecast.name == elem[0].text)
            count = 0
            for ch in res_id_telecast:
                count += 1 
            if count == 0:
                table_telecast = BD.Telecast(name = elem[0].text)
                session.add(table_telecast)
                #session.commit()

            res_id_genre = session.query(BD.Genre.id).filter(BD.Genre.name == elem[1].text)
            count = 0
            for ch in res_id_genre:
                count += 1 
            if count == 0:
                table_genre = BD.Genre(name = elem[1].text)
                session.add(table_genre)
                #session.commit()

            start = parser.parse(elem.get('start'))
            start = start.strftime("%Y-%m-%d %H:%M:%S")

            end = parser.parse(elem.get('stop'))
            end = end.strftime("%Y-%m-%d %H:%M:%S")

            res_id_telecast = session.query(BD.Telecast.id).filter(BD.Telecast.name == elem[0].text)
            for tc in res_id_telecast:
                id_telecast = tc.id

            table_tvprogram = BD.TVprogram(channel = elem.get('channel'), telecast = id_telecast, start_time = start, end_time = end)
            session.add(table_tvprogram)
            #session.commit()
    session.commit()

def search_in_BD(session, channel, nameTV):

    res_id_channel = session.query(BD.Channel.id_channel).filter(BD.Channel.name == channel)
    for ch in res_id_channel:
        id_channel = ch.id_channel 

    date = datetime.now()
    res_id_telecast = session.query(BD.TVprogram.telecast).filter(BD.TVprogram.channel==id_channel).filter(BD.TVprogram.start_time<=date).filter(BD.TVprogram.end_time>=date)

    for tc in res_id_telecast:
        id_telecast = tc.telecast

    res_telecast=session.query(BD.Telecast.name).filter(BD.Telecast.id == id_telecast)
    for tc in res_telecast:
        nameTV.append(tc.name)

    print(nameTV)


