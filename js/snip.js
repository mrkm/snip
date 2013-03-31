var searchCtrl = function($scope, $http){
    var query, jq, hits, i, max, str;
    $scope.search = function(){
        query = {
            "query": {
                "filtered" : {
                    "query" : {
                        "query_string" : {
                            "query" : $scope.query
                        }
                    }
                }
            }
        };
        jq = JSON.stringify(query);
        $scope.jq = jq;
        $http({method: 'GET', url: "http://localhost:9200/murakami/x-python/_search?", data: jq}).
            success(function(data, status, headers, config) {
                // this callback will be called asynchronously
                // when the response is available
                hits = [];
                console.log(status);
                for(i = 0, max = data.hits.hits.length; i < max; i+=1){
                    str = decodeURIComponent(data.hits.hits[i]._source.text);
                    console.log(str);
                    hits.push(str.split(/\r\n|\r|\n/));
                }
                $scope.hits = hits;
            }).
            error(function(data, status, headers, config) {
                // called asynchronously if an error occurs
                // or server returns response with an error status.
                console.log(data);
                console.log(status);
                console.log(headers);
                console.log(config);
            });

    }
};
var configCtrl = function($scope, $http){
    var query, jq;
    $scope.repos = ["lafla.co.jp/svnroot/jglobal_2013", "lafla.co.jp/svnroot/jglobal_2012"]
    $scope.add = function(){
        query = {
            "query": {
                "filtered" : {
                    "query" : {
                        "query_string" : {
                            "query" : $scope.query
                        }
                    }
                }
            }
        };
        jq = JSON.stringify(query);
        console. log(jq);
        $http({method: 'GET', url: "http://localhost:9200/murakami/html/_search?", data: jq}).
            success(function(data, status, headers, config) {
                // this callback will be called asynchronously
                // when the response is available
                $scope.hits = data.hits;
            }).
            error(function(data, status, headers, config) {
                // called asynchronously if an error occurs
                // or server returns response with an error status.
                alert(data);
            });
    }
};