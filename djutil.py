#!/usr/bin/python
# -*- encoding:utf-8 -*-

# kzfm <kerolinq@gmail.com>

import curses
import os
from ScriptingBridge import *

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine,Column,Integer,String,ForeignKey,UniqueConstraint
from sqlalchemy.orm import scoped_session,sessionmaker

database_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'djutil.db')
engine = create_engine('sqlite:///'+database_file)
Session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))
Base = declarative_base(bind=engine)

class Music(Base):
    __tablename__ = 'music'
    __table_args__ = (UniqueConstraint('title','artist'),{})
    id = Column(Integer, primary_key=True)
    title  = Column(String(128))
    artist = Column(String(128))
                     
class Graph(Base):
    __tablename__ = 'graph'
    __table_args__ = (UniqueConstraint('head','tail'),{})
    id = Column(Integer, primary_key=True)
    head = Column(Integer, ForeignKey('music.id'))
    tail = Column(Integer, ForeignKey('music.id'))

def main(stdscr):
    if not os.path.isfile(database_file):
        Base.metadata.create_all()

    session = Session()

    iTunes = SBApplication.applicationWithBundleIdentifier_("com.apple.iTunes")
    stdscr.nodelay(1)
    head_music = None
    tail_music = None

    while True:
        c = stdscr.getch()
        y,x = stdscr.getyx()
        if c == ord('h'):
            artist = iTunes.currentTrack().artist()
            title  = iTunes.currentTrack().name()
            head_music = session.query(Music).filter(Music.artist == artist) \
                                             .filter(Music.title == title) \
                                             .first()
            if head_music == None:
                head_music = Music(artist=artist,title=title)
                session.add(head_music)
                session.commit()

            if tail_music != None:
                mg = session.query(Graph).filter(Graph.head == head_music.id) \
                                             .filter(Graph.tail == tail_music.id) \
                                             .first()
                if mg == None:
                    mg = Graph(head=head_music.id,tail=tail_music.id)
                    session.add(mg)
                    session.commit()

                stdscr.addstr("%s / %s -> %s / %s" % (head_music.title,head_music.artist,tail_music.title,tail_music.artist))
                stdscr.move(y+1, 0)

                tail_music = None
            else:
                stdscr.addstr("%s / %s -> [] / []" % (head_music.title.encode('utf-8'),head_music.artist.encode('utf-8')))
                stdscr.move(y, 0)
                
        elif c == ord('t'):
            artist = iTunes.currentTrack().artist()
            title  = iTunes.currentTrack().name()
            tail_music = session.query(Music).filter(Music.artist == artist) \
                                .filter(Music.title == title) \
                                .first()

            if tail_music == None:
                tail_music = Music(artist=artist,title=title)
                session.add(tail_music)
                session.commit()

            if head_music != None:
                mg = session.query(Graph).filter(Graph.head == head_music.id) \
                                             .filter(Graph.tail == tail_music.id) \
                                             .first()
                if mg == None:
                    mg = Graph(head=head_music.id,tail=tail_music.id)
                    session.add(mg)
                    session.commit()

                stdscr.addstr("%s / %s -> %s / %s" % (head_music.title.encode('utf-8'),head_music.artist.encode('utf-8'),tail_music.title.encode('utf-8'),tail_music.artist.encode('utf-8')))
                stdscr.move(y+1, 0)
                tail_music = None

            else:
                stdscr.addstr("[] / [] -> %s / %s" % (tail_music.title,tail_music.artist))
                stdscr.move(y, 0)
        elif c == ord('q'):
            break
        elif c != -1:
            # debug
            stdscr.addstr(str(c))
            stdscr.refresh()
            stdscr.move(0, 0)

if __name__ == '__main__':
    curses.wrapper(main)
