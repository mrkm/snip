var searchCtrl = function($scope, $http){
    var query, jq, hits, i, max, str;
    $scope.search = function(){
	query = {	    
	    "fields": "text",
            "q": "text:" + $scope.query	
        };
        //jq = JSON.stringify(query);
        //$http({method: 'GET', url: "http://localhost:9200/murakami/x-python/_search?", data: jq}).
        $http({method: 'GET', url: "http://localhost:9200/murakami/css/_search?fields=text", params: query}).
            success(function(data, status, headers, config) {
                // this callback will be called asynchronously
                // when the response is available
                hits = [];
                for(i = 0, max = data.hits.hits.length; i < max; i+=1){
                    str = decodeURIComponent(data.hits.hits[i].fields.text);
                    hits.push(str.split(/\r\n|\r|\n/));
                }
                $scope.hits = hits;
		$scope.hitnum = hits.length;
            }).
            error(function(data, status, headers, config) {
                // called asynchronously if an error occurs
                // or server returns response with an error status.
		if(status == 0){$scope.error="Connection refused."}
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