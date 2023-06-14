document.addEventListener('DOMContentLoaded', function() {
    var wrapper = document.createElement('div');
    wrapper.innerHTML = "<div class=\"admonition warning\">" +
        "<p class=\"admonition-title\">Warning</p>" +
        "<p>This is the documentation for pre-release version " +
        DOCUMENTATION_OPTIONS.VERSION +
        " of the IBM Z CICS Collection.</p>" +
        "<p>Alternatively, see the <a href=\"https://ibm.github.io/z_ansible_collections_doc/\">latest stable version documentation</a>.</p>" +
        "</div>";
    document.querySelector("div[itemprop='articleBody']").prepend(wrapper.firstChild);
}, false);