(function() {
    var RealTimeData = function(tunnelName) {
        this.tunnelName = tunnelName;
        this.timestamp = ((new Date()).getTime() / 1000)|0;
    };

    RealTimeData.prototype.history = function() {
        var history = [
            { label: 'rx_pkts', values: []},
            { label: 'tx_pkts', values: []}
        ];
        for (var i = 0; i < history.length; i++) {
            history[i].values.push({time: this.timestamp, y: 0});
            this.timestamp--;
        }
        return history;
    }

    RealTimeData.prototype.next = function() {
        var next = [];
        $.ajax({
            type: "get",
            url: "/api/vpn/" + this.tunnelName + "/traffic/now",
            async: false,
            cache: false,
            success: function(res, status, xhr) {
                next.push({time: res.time, y: res.tx_pkts});
                next.push({time: res.time, y: res.rx_pkts});
            }
        });
        return next;
    }
    window.RealTimeData = RealTimeData;
})();
