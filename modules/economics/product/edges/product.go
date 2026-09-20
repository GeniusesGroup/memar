/* For license and copyright information please see the LEGAL file in the code repository */

package label

type Field_Type interface {
	ProductType() Type
}

// Cinema, Rent, Therapy, Consulting, Coaching, Mentoring, FixingService, the transportation of goods and passenger,  ...
type Type uint64

const Type_Unset Type = 0 // usually for good kind

// Common flags
const (
	Type_Good             Type = (1 << iota) // if flag not set means product is service
	Type_ReserveValidity                     //
	Type_ReserveQuantity                     // max product can reserve by one person before pay them
	Type_PreSale                             // ??
	Type_NeedApprove                         // base on product-role
	Type_NeedPrescription                    // Medical good. can't add by users to invoice

	Type_InvoiceSell     //
	Type_OrderSell       //
	Type_SellLimit_Role  // base on product-role
	Type_SellLimit_Group // group limit sell
	Type_SellLimit_User  // user limit sell
)

// Good flags
const (
	Type_Inventory        // usually capital good must track owner. Book, Mobile, Car, ...
	Type_Custom           // made on buyer requirements, product-ingredient
	Type_BestBefore       // Consumption good. any Good usually use daily to satisfy human wants.
	Type_CustomIngredient //
)

// Services flags
// Service is the structure of TimeService like:
// Consultation in chat or real life
// It can yse for any service or goods e.g.
// ActService like guarding, maintenance, cleaning, ...
// Transport
const (
	Type_TimeValidity  
	Type_Transport           // indicate InvoiceID use to retrieve coordinate domain
	Type_Shipping            //
	Type_Content             // for any content types, Digital data
	Type_Timing              // the time service will provide
	Type_TimingInterval      //
	Type_MultipleUse         // gym, ...
	Type_Duration            //
	Type_Number              // cinema, concert, transport, ...
	Type_Area                // transport, ...
	Type_Place               // limit to get service on specific place like doctor-room, gym, station(bus, train, airport, ...)
	Type_Seat                // cinema, concert, transport, ...
	Type_Provider_Staff      // the provider of the product
	Type_Provider_Role       // the provider of the product
	Type_Share               // ticket for panic room, ...
)
