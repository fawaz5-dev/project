(function () {
    const button = document.createElement('div');
    button.style.position = 'fixed';
    button.style.bottom = '20px';
    button.style.right = '20px';
    button.style.width = '60px';
    button.style.height = '60px';
    button.style.borderRadius = '50%';
    button.style.backgroundImage = 'url("{{logo}}")';
    button.style.backgroundSize = 'cover';
    button.style.backgroundColor = '#ccc';  // temporary
    button.style.cursor = 'pointer';
    button.style.zIndex = '1000';
    document.body.appendChild(button);

    const iframe = document.createElement('iframe');
    iframe.src = "{{iframe_url}}";
    iframe.style.position = 'fixed';
    iframe.style.bottom = '90px';
    iframe.style.right = '20px';
    iframe.style.width = '400px';
    iframe.style.height = '500px';
    iframe.style.border = 'none';
    iframe.style.borderRadius = '12px';
    iframe.style.boxShadow = '0 0 12px rgba(0,0,0,0.2)';
    iframe.style.display = 'none';
    iframe.style.zIndex = '999';
    document.body.appendChild(iframe);

    button.addEventListener('click', () => {
        iframe.style.display = (iframe.style.display === 'none') ? 'block' : 'none';
    });
})();

