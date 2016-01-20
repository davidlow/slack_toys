"""
SlackSaver, saves channel, user, data from Slack.
"""

from slacker import Slacker;
import pickle

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
        for n in range(numtry):
            users = self.slack.users.list();
            usersdict = users.__dict__;
            if(usersdict['successful'] and
               usersdict['body']['ok']       ):
                with open(savefilename + '.pickle', 'w') as f:
                    userlookup = {};
                    for member in usersdict['body']['members']:
                        userlookup[member['id']] = {
                                'name':     member['name'],
                                'real_name':member['real_name'],
                                }
                    pickle.dump([users, userlookup], f);
                error.append(0);
                return error;
            else:
                error.append(usersdict['error'])
        return error;
    
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
                with open(savefilename + '.pickle', 'w') as f:
                    channellookup = {};
                    for ch in channelsdict['body']['channels']:
                        userlookup[ch['id']] = {
                                'name':     ch['name'],
                                'purpose':member['purpose'],
                                }
                    pickle.dump([channels, channellookup], f);
                error.append(0);
                return error;  
            else:
                error.append(usersdict['error'])
        return error;

    def getchhist(self, savefilename, channelid, tstart, tstop, 
            numtry = 10):
        for n in range(numtry):
            hist = self.slack.channels.history(channelid); #TODO: add t's
            histdict = hist.__dict__;
            if(histdict['successful'] and 
               histdict['body']['ok']    ):
                with open(savefilename + '.pickle', 'w') as f:
                    
