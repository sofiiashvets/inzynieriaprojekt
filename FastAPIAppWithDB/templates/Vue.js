var app = new Vue(
    {
        el:'#app',
        data: {
            message: "Hello Vue",
            counter: 0,
            users: [{name: "Ada"},{name: "Szymon"}]
        },
        
        // watch: { //wykrywa zmiane zmiennych
        //     counter(){
        //         alert("counter was updated")
        //     }

        // },

        methods: {
            increaseCounter()
            {
                this.counter++
            },

            decreaseCounter()
            {
                this.counter--
            }

        }
    }
);

app.message = "xdsadD"
