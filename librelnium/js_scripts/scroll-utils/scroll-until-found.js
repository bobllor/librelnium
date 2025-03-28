window.scrollUntilFound = (scrollY = null, scrollX = null, webElement, limit = 15) => {
    const throwTypeError = (message) => {throw new TypeError(message)}
    
    if(scrollY === null && scrollX === null){
        throwTypeError('Must pass an Element to either scrollY or scrollX.')
    }

    if(scrollY != null && scrollY.nodeType != 1){
        throwTypeError(`Expected scrollY to be a Element node or null, got ${typeof scrollY}`)
    }

    if(scrollX != null && scrollX.nodeType != 1){
        throwTypeError(`Expected scrollX to be a Element node or null, got ${typeof scrollX}`)
    }

    if(webElement.nodeType != 1){
        throwTypeError(`Expected webElement to be Element node, got ${typeof webElement}`)
    }

    let count = 0;

    let id = setInterval(() => {
        let elementVisibility = webElement.checkVisibility();

        if(count === limit || elementVisibility === true){
            if(elementVisibility === true){
                console.log('found');
            }
            
            clearInterval(id);
        }

        if(scrollY != null){
            scrollY.scrollBy(0, 100);
        }

        if(scrollX != null){
            scrollX.scrollBy(100, 0);
        }
 
        count++;
    }, 500)
}