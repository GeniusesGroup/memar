




const storePage = {
    mediaType: ,
    status: ,
    robots: ,
    icon: ,
    info: {
        language: ,
        name: ,
        shortName: ,
        tagline: ,
        slogan: ,
        description: ,
        tags: ,
    },
    relatedPages: ,
    path: ,
    acceptedCondition: ,
    activeState: ,
    activeStates: ,
    createState: ,
    
};


const storePageState = {
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
storePage.defineProperty(storePage, "mediaType", {
    get : function () {
        return this.mediaType;
    }
});

// setting property
storePage.defineProperty(storePage, "mediaType", {
    set : function (value) {
        this.mediaType = value;
    }
});