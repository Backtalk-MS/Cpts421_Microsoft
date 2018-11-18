var mongoose = require('mongoose');
var fs = require('fs');
var files = []

fs.readdirSync("./json/").forEach(file => files.push(file));

mongoose.connect("mongodb://aminich:5WOXsas5o8bQVSIapi3i4fH6jAZGD7hSu2EvmjqP0HbxlB0PFXRK1OnKihWu26YHltGxkXfQSVasw4hFaLp9xw==@aminich.documents.azure.com:10255/?ssl=true&replicaSet=globaldb", {
    auth: {
      user: "aminich",
      password: "5WOXsas5o8bQVSIapi3i4fH6jAZGD7hSu2EvmjqP0HbxlB0PFXRK1OnKihWu26YHltGxkXfQSVasw4hFaLp9xw=="
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
