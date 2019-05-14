# Team 20
# Team member: Site Huang, 908282
#              Chenyuan Zhang, 815901
#              Zixuan Zhang, 846305
#              Zhentao Zhang, 864735
#              Kangyun Dou, 740145
import couchdb


class viewGenerator:
    def __init__(self, server_ip, username, password, dataDB):
        serverFullAddress = 'http://%s:%s@%s:5984/' % (username, password, server_ip)
        self.server = couchdb.Server(serverFullAddress)
        self.dataDB = self.server[dataDB]
        try:
            self.resultDB = self.server['result_' + dataDB]  # if database has already created
        except couchdb.http.ResourceNotFound as e:
            self.resultDB = self.server.create('result_' + dataDB)  # First time
            self.resultDB = self.server['result_'+dataDB]

        self.allView = {
            'get_wrath_score': {
                'map': 'function(doc){emit(doc.place.full_name, doc.wrath_score);}',
                'reduce': '''
            function (keys, values, rereduce) {
              var result = 0;
              var count = 0;
              if (rereduce){
                values.forEach(function(vObj){
                  result += vObj.result;
                  count += vObj.count;
                });
              }else{
                values.forEach(function(v){
                  result += v;
                  count += 1;
                })
              }
              return ({result: result, count: count});
            }
            '''
            },
            'get_pride_score': {
                'map': 'function(doc){emit(doc.place.full_name, {followers: doc.user.followers_count, textlength: doc.text.split(" ").length, favourites: doc.user.favourites_count, retweet: doc.retweet_count+1});}',
                'reduce': '''
            function (keys, values, rereduce) {
              var result = 0;
              var count = 0;
              if (rereduce){
                values.forEach(function(vObj){
                  result += vObj.result;
                  count += vObj.count;
                });
              }else{
                values.forEach(function(vObj){
                  result += vObj.followers*vObj.textlength*vObj.retweet/vObj.favourites;
                  count += 1;
                })
              }
              return ({result: result, count: count});
            }
            '''
            },
            'get_hashtag_sum': {
                'map': 'function(doc){for(var i=0; i<doc.entities.hashtags.length;i++){tmp = doc.entities.hashtags[i].text.toLowerCase(); emit([tmp, doc.place.full_name], 1);}}',
                'reduce': 'function(keys, values){return sum(values);}'
            }
        }
        self.generateView()

    def generateView(self):
        try:
            self.dataDB['_design/summary'] = dict(language='javascript', views=self.allView)
        except:
            del self.dataDB['_design/summary']
            self.dataDB['_design/summary'] = dict(language='javascript', views=self.allView)

    def updateView(self):
        try:
            data = self.resultDB.get('0')
            if not data:
                data = {'_id': '0'}
            data['wrath_score'] = {}
            for item in self.dataDB.view('summary/get_wrath_score', group=True):
                data['wrath_score'][item.key] = item.value
            data['pride_score'] = {}
            for item in self.dataDB.view('summary/get_pride_score', group=True):
                data['pride_score'][item.key] = item.value
            data['hashtag'] = {}
            for item in self.dataDB.view('summary/get_hashtag_sum', group=True, group_level=2):
                if item.key[1] not in data['hashtag']:
                    data['hashtag'][item.key[1]] = {}
                data['hashtag'][item.key[1]][item.key[0]] = item.value
            data['hashtag_total'] = {}
            for item in self.dataDB.view('summary/get_hashtag_sum', group=True, group_level=1):
                data['hashtag_total'][item.key[0]] = item.value
            self.resultDB.update([data])
        except:
            pass
