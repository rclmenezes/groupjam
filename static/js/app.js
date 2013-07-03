//
// Models
//

User = Backbone.Model.extend({
    urlRoot: '/user'
})

Post = Backbone.Model.extend({
    initialize: function(attributes, options) {
        this.options = options;
    }
});

PostList = Backbone.Collection.extend({
    model: Post,
    
    initialize: function(models, options) {
        this.id = options.id;
    },
    
    url: function(){
        return "/thread/" + this.id + "/posts";
    }
});

Thread = Backbone.Model.extend({
    urlRoot: '/thread',
    
    defaults: {
        user_id: -1,
        subject: '',
        posts: new PostList([], {id: this.id})
    },
    
    set: function(attributes, options) {
        if (attributes.posts !== undefined && !(attributes.posts instanceof PostList)) {
                attributes.posts = new PostList(attributes.posts, {id: this.id});
            }
        return Backbone.Model.prototype.set.call(this, attributes, options);
    }
});

//
// Views
//

PostView = Backbone.View.extend({
    initialize: function(options){
        this.template_variables = $.extend({}, this.model.options, this.model.attributes);
        this.post_editor_view = options.post_editor_view;
        this.render();
    },
    render: function(){
        var template = _.template( $("#post_template").html(), this.template_variables );
        this.$el.html( template );
    },
    events: {
        "click .add_share": "add_share",
        "click .add_kudos": "add_kudos"
    },
    add_share: function(event){
        console.log("Add share");
    },
    add_kudos: function(event){
        console.log("Add kudos");
    }
});

ThreadView = Backbone.View.extend();

EditorBaseView = Backbone.View.extend({
    initialize: function(options){
        this.template_variables = { 
            placeholder_text: this.placeholder_text, 
            profile_picture: options.user.get('profile_picture')
        };
        this.render();
        this.savedSel = null;
    },
    render: function(){
        var template = _.template( $("#editor_template").html(), this.template_variables );
        this.$el.html( template );
    },
    events: {
        "click .post_editor_before .post_editor_input": "editor_activate",
        "click .post_editor_placeholder": "focus_input",
        "mousedown .post_button": "post_button_down",
        "mouseup .add_image": "add_image",
        "mouseup .add_file": "add_file",
        "mouseup .add_link": "add_link",
        "click .link_modal .save_changes": "save_link",
        "click .submit": "save_model"
    },
    editor_activate: function(event){
        this.$el.find('.post_editor_before').hide();
        this.$el.find('.post_editor_after').show();
        this.$el.find('.post_editor_after .post_editor_input').focus();
    },
    focus_input: function(event){
        this.$el.find('.post_editor_after .post_editor_input').focus();
    },
    post_button_down: function(event){
        if (this.$el.find('.post_editor_after .post_editor_input').is(':focus'))
        {
            event.preventDefault();
            return false;
        }
    },
    add_image: function(event){
        if (this.$el.find('.post_editor_after .post_editor_input').is(':focus'))
        {
            this.savedSel = saveSelection();
        }
        else
        {
            this.editor_activate(event);
        }
        this.$el.find('.image_modal').modal();
    },
    add_link: function(event){
        if (this.$el.find('.post_editor_after .post_editor_input').is(':focus'))
        {
            this.savedSel = saveSelection();
        }
        else
        {
            this.editor_activate(event);
        }
        this.$el.find('.link_modal').modal();
    },
    add_file: function(event){
        if (this.$el.find('.post_editor_after .post_editor_input').is(':focus'))
        {
            this.savedSel = saveSelection();
        }
        else
        {
            this.editor_activate(event);
        }
        this.$el.find('.file_modal').modal();
    },
    // make_bold: function(event){
    //     if (this.$el.find('.post_editor_after .post_editor_input').is(':focus'))
    //     {
    //         this.$el.find('.make_bold').toggleClass('post_button_active');
    //         document.execCommand('StyleWithCSS', false, false);
    //         document.execCommand("bold", false, 800);

    //         this.$el.find('.post_editor_after .post_editor_input').css('font-weight', 'bold');
    //     }
    // },
    // make_italic: function(event){
    //     if (this.$el.find('.post_editor_after .post_editor_input').is(':focus'))
    //     {
    //         this.$el.find('.make_italic').toggleClass('post_button_active');
    //         document.execCommand('StyleWithCSS', false, false);
    //         document.execCommand("italic", false, null);
    //     }
    // },
    // make_underline: function(event){
    //     if (this.$el.find('.post_editor_after .post_editor_input').is(':focus'))
    //     {
    //         this.$el.find('.make_underline').toggleClass('post_button_active');
    //         document.execCommand('StyleWithCSS', false, false);
    //         document.execCommand("underline", false, null);
    //     }
    // },
    save_link: function(event){
        var link = this.$el.find('.link_modal #link_url').val();
        var email_regex = /^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;
        if (email_regex.test(link))
        {    
            link = "mailto:" + link;
        }
        else if (link.substr(0,7) != "mailto:" && link.substr(0,7) != "http://" && link.length != 0)
        {
            link = "http://" + link;
        }

        if (this.savedSel != null)
            restoreSelection(this.savedSel);
        else
            this.$el.find('.post_editor_after .post_editor_input').focus();

        document.execCommand('StyleWithCSS', false, false);
        document.execCommand("CreateLink", false, link);
        this.$el.find('.link_modal').modal('hide');
    }
});

ThreadEditorView = EditorBaseView.extend({
    initialize: function(options){
        this.placeholder_text = "Start a thread...";
        this.constructor.__super__.initialize.apply(this, [options]);
        this.$el.find(".group_select").select2({
            containerCssClass: "group_select_container",
            placeholder: "Select a group..."
        });
    },
    events: function(){
        return _.extend({}, EditorBaseView.prototype.events,{
            'input .post_editor_after .post_editor_input': 'post_titler'
        });
    },
    post_titler: function(){
        var content = this.$el.find('.post_editor_after .post_editor_input').html();
        if (content.length == 0 || content == "<br>")
        {
            this.$el.find('.post_editor_placeholder').show();
        }
        else
        {
            this.$el.find('.post_editor_placeholder').hide();
        }
    },
    save_model: function(event){
        this.model.save();
    }
});

PostEditorView = EditorBaseView.extend({
    initialize: function(options){
        this.placeholder_text = "Add your thoughts...";
        this.constructor.__super__.initialize.apply(this, [options]);
        this.$el.find(".group_select").hide();
        this.$el.find(".post_editor_placeholder").hide();
        this.$el.find(".thread_important").hide();
        this.$el.find("label.send_email").hide();
    },
    save_model: function(event){
        this.model.save({ content: this.$el.find('.post_editor_after .post_editor_input').html() });
    }
});

// http://stackoverflow.com/a/2925633/764463
function saveSelection() {
    if (window.getSelection) {
        sel = window.getSelection();
        if (sel.getRangeAt && sel.rangeCount) {
            var ranges = [];
            for (var i = 0, len = sel.rangeCount; i < len; ++i) {
                ranges.push(sel.getRangeAt(i));
            }
            return ranges;
        }
    } else if (document.selection && document.selection.createRange) {
        return document.selection.createRange();
    }
    return null;
}

function restoreSelection(savedSel) {
    if (savedSel) {
        if (window.getSelection) {
            sel = window.getSelection();
            sel.removeAllRanges();
            for (var i = 0, len = savedSel.length; i < len; ++i) {
                sel.addRange(savedSel[i]);
            }
        } else if (document.selection && savedSel.select) {
            savedSel.select();
        }
    }
}