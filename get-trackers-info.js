ga(function() {
    var trackersInfo = [];

    // Get all the GA tracker objects on the page
    var allTrackers = ga.getAll();

    for (var i = 0; i < allTrackers.length; i++) {
        var t = allTrackers[i];
        var tData = t.a.data.values;
        var tName = tData[':name'];
        var tTrackingId = tData[':trackingId'];
        var tClientId = tData[':clientId'];

        trackersInfo.push({
            'name': tName,
            'trackingId': tTrackingId,
            'clientId': tClientId
        });

        // console.log(t.ad.data.values);
    }

    console.table(trackersInfo);
});


// Get client ID for a tracker by Name
ga(function() {
    ga.getByName('gtm3').get('clientId');
});