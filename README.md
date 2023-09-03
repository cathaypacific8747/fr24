# fr24

Download and parse data from flightradar24.com with gRPC.
For educational and research purposes only.

# References

https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-HTTP2.md

Notes:
```js
uc(o, l, i); // vendor bp @ 27660:9 f
copy(btoa(String.fromCharCode.apply(null, i))); // i: Uint8Array

w = await Po() // index bp @ 29516:8 f

dbName = "MobileCountries" // AircraftFamily, Airlines, Airports, MobileCountries
request = indexedDB.open(dbName)
request.onsuccess = function(event) {
  const db = event.target.result;
  const transaction = db.transaction(dbName, 'readonly');
  const objectStore = transaction.objectStore(dbName);
  const request = objectStore.getAll();

  request.onsuccess = function(event) {
    console.log(JSON.stringify(event.target.result))
  };
};
```