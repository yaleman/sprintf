var sprintf = new Vue({
    el: '#sprintf',
    data: {
        formatstring: '%Y-%m-%dT%H:%M:%S', // set the default value
        outputval: ''
    },
    created () {
        this.getParsed();
    },
    watch: {
        formatstring() {
            // watch the formatstring input and update the parsed result
            this.getParsed();
        },
    },
    methods: {
        copy_formatstring: function() {
            navigator.clipboard.writeText.clipboard.writeText(this.formatstring);
        },
        copy_output: function() {
            navigator.clipboard.writeText.clipboard.writeText(this.output);
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

