



const productPage = {
  mediaType: "",
  status: '',
  robots: "",
  icon: "",
  info: {
    language: "english",
    name: "product",
    shortName: "",
    tagline: "",
    slogan: "",
    description: "",
    tags: [],
  },
  relatedPages: [use-page, invoice-page],
  path: "/product",
    acceptedCondition: {
        id: '', // productId
  },
  activeState: '',
  activeStates: '',
  createState: '',
};


const productPageState = {
    page: '',
    url: '/product?p=1234',
    title: '',
    description: '',
    conditions: '',
    fragment: '',
    createDate: '',
    lastActiveDate: '',
    endDate: '',
    dom: '',
    som: '',
    thumbNail: '',
    activate: '',
    deActivate: '',
    refresh: '',
    safeToSilentClose: bool ,
    close: '',
};




// The Object.defineProperty() method takes three arguments.

// The first argument is the objectName.
// The second argument is the name of the property.
// The third argument is an object that describes the property.

// getting property
productPage.defineProperty(productPage, "mediaType", {
    get : function () {
        return this.mediaType;
    }
});

// setting property
productPage.defineProperty(productPage, "mediaType", {
    set : function (value) {
        this.mediaType = value;
    }
});


// https://en.wikipedia.org/wiki/Software_release_life_cycle

// 	// Software_PreAlpha refers to all activities performed during the software project before formal testing.
// 	Software_PreAlpha 
// 	// Software_Alpha is the first phase to begin software testing
// 	Software_Alpha
// 	// Software_Beta generally begins when the software is feature complete but likely to contain a number of known or unknown bugs.
// 	Software_Beta
// 	// Software_PerpetualBeta where new features are continually added to the software without establishing a final "stable" release.
// 	// This technique may allow a developer to delay offering full support and responsibility for remaining issues.
// 	Software_PerpetualBeta
// 	// Software_OpenBeta is for a larger group, or anyone interested.
// 	Software_OpenBeta
// 	// Software_ClosedBeta is released to a restricted group of individuals for a user test by invitation.
// 	Software_ClosedBeta
// 	// Software_ReleaseCandidate also known as "going silver", is a beta version with potential to be a stable product,
// 	// which is ready to release unless significant bugs emerge
// 	Software_ReleaseCandidate
// 	// Software_StableRelease Also called production release,
// 	// the stable release is the last release candidate (RC) which has passed all verifications / tests.
// 	Software_StableRelease
// 	// Software_EndOfLife indicate no longer supported and continue its existence until to ExpiryDate!
// 	Software_EndOfLife
