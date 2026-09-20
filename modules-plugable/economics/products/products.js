


const productsPage = {
    mediaType: ,
    status: ,
    robots: ,
    icon: ,
    info: ,
    relatedPages: ,
    path: ,
    acceptedCondition: ,
    activeState: ,
    activeStates: ,
    createState: ,
    
};


const ProductsPageState = {
    page: ,
    url: ,
    title: ,
    description: ,
    conditions: ,
    fragment: ,
    createDate: ,
    lastActiveDate: ,
    endDate: ,
    dom: ,
    som: ,
    thumbnail: ,
    activate: ,
    deactivate: ,
    refresh: ,
    safeToSilentClose: ,
    close: ,
};


// The Object.defineProperty() method takes three arguments.

// The first argument is the objectName.
// The second argument is the name of the property.
// The third argument is an object that describes the property.

// getting property
productsPage.defineProperty(productsPage, "mediaType", {
    get : function () {
        return this.mediaType;
    }
});

// setting property
productsPage.defineProperty(productsPage, "mediaType", {
    set : function (value) {
        this.mediaType = value;
    }
});