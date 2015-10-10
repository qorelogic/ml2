
use ql22b;
db.dropDatabase();
use ql22;
db.copyDatabase("ql22","ql22b","localhost:27018");
