// update URL functionality based on this: https://www.raymondcamden.com/2021/05/08/updating-and-supporting-url-parameters-with-vuejs

var sprintf = new Vue({
    el: '#sprintf',
    data: {
        formatstring: '%Y-%m-%dT%H:%M:%S', // set the default value
        outputval: ''
    },
    created () {
        let qp = new URLSearchParams(window.location.search);
        if (qp.get("f") != "" && qp.get("f") != null ) {
            this.formatstring = qp.get("f");
        }
        this.getParsed();
    },
    watch: {
        // watch the formatstring input and update the parsed result
        formatstring() {
            this.getParsed();
            this.updateUrl();
        },
    },
    methods: {
        updateUrl() {
            let qp = new URLSearchParams();
            if(this.formatstring !== '') {
                qp.set('f', this.formatstring);
            } else {
                qp.set("f", "");
            }
            history.replaceState(null, null, "?"+qp.toString());
        },
        getParsed: function() {
            axios.post(
                "/parse",
                { formatstring: this.formatstring }
            ).then(res => {
                this.outputval = res.data.result;
            });
        }
    },
  })

