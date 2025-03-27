window.isScrollable = () => {
    let element = document.querySelector('body');

    let overflowValue = window.getComputedStyle(element).getPropertyValue('overflow');

    if(overflowValue != 'hidden'){
        return true;
    }

    return false;
}