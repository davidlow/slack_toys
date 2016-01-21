"""
SlackSaver, saves channel, user, data from Slack.
Data saved in json format.  To read, cat *.json | python -m json.tool
"""

from slacker import Slacker;
from collections import deque;
import pickle
import json
from time import ctime


class SlackSaver:
    """ Slack Saver; saves slack info"""

    def __init__(self, token):
        """
        Get token from: https://api.slack.com/web
        """
        self.slack = Slacker(token);

    def getallusers(self, savefilename, numtry = 10):
        """ gets all users and saves the raw and a dict with 
            key = their id and 
            value = {'name': name, 'real_name': real_name}
        """
        users = {};
        error = [];
        userlookup = {};
        for n in range(numtry):
            users = self.slack.users.list();
            usersdict = users.__dict__;
            if(usersdict['successful'] and
               usersdict['body']['ok']       ):
                for member in usersdict['body']['members']:
                    userlookup[member['id']] = {
                        'name':     member['name'],
                        'real_name':member['real_name'],
                    }
                with open(savefilename + '.json', 'w') as f:
                    json.dump([usersdict, userlookup], f);
                error.append(0);
                return [userlookup, error];
            else:
                error.append(usersdict['error'])
        return [userlookup, error];
    
    def getallchannels(self, savefilename, numtry = 10):
        """ gets all channels and saves the raw and a dict with 
            key = channel id and 
            value = {'name': name, 'purpose': real_name}
        """
        channels = {};
        error    = [];
        for n in range(numtry):
            channels = self.slack.channels.list();
            channelsdict = channels.__dict__;
            if(channelsdict['successful'] and 
               channelsdict['body']['ok']       ):
                with open(savefilename + '.json', 'w') as f:
                    channellookup = {};
                    for ch in channelsdict['body']['channels']:
                        channellookup[ch['id']] = {
                                'name':     ch['name'],
                                'purpose':  ch['purpose'],
                                }
                    json.dump([channelsdict, channellookup], f);
                error.append(0);
                return error;  
            else:
                error.append(usersdict['error'])
        return error;

    def getchhist(self, savefilename, channelid, tstart, tstop, 
            userlookup,
            numtry = 10):
        error = [];
        times = deque();
        times.append((tstart, tstop));
        allmessages = [];
        while(len(times) != 0):
            thistime = times.popleft();
            for n in range(numtry):
                hist = self.slack.channels.history( channelid, 
                        latest = thistime[1],
                        oldest = thistime[0]
                        ); 
                histdict = hist.__dict__;
                if(histdict['successful'] and 
                   histdict['body']['ok']    ):
                    if(histdict['body']['has_more']):
                        times.appendleft(
                        (thistime[0] + (thistime[1] - thistime[0])/2, 
                         thistime[1]
                        ))
                        times.appendleft(
                        (thistime[0], thistime[0] + 
                         (thistime[1] - thistime[0])/2
                        ))
                    else:
                        allmessages = (
                                histdict['body']['messages'][::-1]  + 
                                allmessages );
                        break;
        info = [];
        for n in range(numtry):
            rawinfo = self.slack.channels.info(channelid).__dict__;
            if(rawinfo['successful'] and 
               rawinfo['body']['ok'] ):
                info = rawinfo['body']['channel'];
                break;
        with open(savefilename + '.json', 'w') as f:
            json.dump([info, allmessages], f)

        csv = [];
        for m in allmessages:
            name = '';
            try:
                name = str(userlookup[m['user']]);
            except:
                try:
                    name = str(m['username']);
                except:
                    name = '';
            message = '';
            try:
                message = str(m['text']);
            except:
                message = 'Type = ' + str(m['type']);
            csv.append( ( ctime(float(m['ts'])), name, message) );
        with open(savefilename + '.csv', 'w') as f:
            for c in csv:
                print(c);
                f.write(c[0] + ', ' + c[1] + ', ' + c[2] + '\n')
        return error;

                            
                   
