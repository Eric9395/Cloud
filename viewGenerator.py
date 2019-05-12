import couchdb


class viewGenerator:
    def __init__(self, server_ip, username, password, dataDB):
        serverFullAddress = 'http://%s:%s@%s:5984/' % (username, password, server_ip)
        self.server = couchdb.Server(serverFullAddress)
        self.dataDB = self.server[dataDB]
        try:
            self.resultDB = self.server.create('result')  # First time
        except:
            self.resultDB = self.server['result']  # if database has already created

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
                'map': 'function(doc){for(var i=0; i<doc.hashtags.length;i++){emit([doc.place.full_name,doc.hashtags[i].text], 1);}}',
                'reduce': 'function(keys, values){return sum(values);}'
            }
        }

    def generateView(self):
        try:
            self.dataDB['_design/summary'] = dict(language='javascript', views=self.allView)
        except:
            del self.dataDB['_design/summary']
            self.dataDB['_design/summary'] = dict(language='javascript', views=self.allView)

    def updateView(self):
        data = self.resultDB['wrath_score']
        for index, item in enumerate(self.dataDB.view('summary/get_wrath_score', group=True)):
            data[index] = item
        self.resultDB.save(data)

        data = self.resultDB['pride_score']
        for index, item in enumerate(self.dataDB.view('summary/get_pride_score', group=True)):
            data[index] = item
        self.resultDB.save(data)

        data = self.resultDB['hashtag']
        for index, item in enumerate(self.dataDB.view('summary/get_pride_score', group=True, group_level=2, descending=True, limit=50)):
            data[index] = item
        self.resultDB.save(data)
