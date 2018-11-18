var mongoose = require('mongoose');
var fs = require('fs');
var files = []

fs.readdirSync("./json/").forEach(file => files.push(file));

mongoose.connect("#URI HERE#", {
    auth: {
      user: "#USERNAME HERE#",
      password: "#PASSWORD HERE#"
    },
    useNewUrlParser: true
  })
  .then(() => console.log('Connection to CosmosDB successful'))
  .catch((err) => console.error(err));

var postSchema = new mongoose.Schema({
    title: String,
    maincategory: String,
    subcategory: {type: String, default: ""},
    subjects: [String],
    content: String
});

var Post = mongoose.model('Post',postSchema);


files.forEach(file => {
    var fileContent = fs.readFileSync("json/"+file);
    var parsedContent = JSON.parse(fileContent);

    var posts = []

    parsedContent.forEach(function(elem){
        var post = new Post({
            title: elem.title,
            maincategory: elem.category,
            subcategory: elem.subcategory,
            subjects: elem.subjects,
            content: elem.content
        });
        posts.push(post)
        // post.save(function(err){
        //     if(err) throw err;
        //     console.log("Successfully inserted "+elem.title);
        // });
        
        // console.log(elem.title);
        // console.log(elem.content);
    });

    console.log("Insertion starting");
    Post.insertMany(posts)
        .then(()=> console.log("One batch insert complete"))
        .catch((error)=> {
            console.log(error);
        });
});
