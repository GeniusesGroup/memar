/* For license and copyright information please see the LEGAL file in the code repository */

package upp

import (
	pp "org/modules/product/protocol"
)

type GUI_Page_UsedDomains interface {
	// Product
	// Quiddity
	// Category
	// Warehouse
}

type GUI_Page_HyperLinks interface {
	NavigateToProductPage()
}

type GUI_Page_Conditions interface {
	ProductType() pp.Type
	OrgID()
	OrgType() // Privilege, Official, county, ...
	Brand()
	CategoryID()
	Text()
	WarehouseID()
	StaffID()
	RoleID()

	Estate()             // MUST set user location as default
	BuildingID()         // MUST set user location as default
	BuildingLocationID() // MUST set user location as default

	// Filter:
	OutStock() bool // != InStock
	// Price()
	// Discount()
	MostLiked() bool
	Used() // New, MostlyNew, Refurbished, ...
	// MostSell()
	// MostViewed()
	// Complement()
	// Subsitute()
	// Sort()
	// WarehousePreference() close to me, send imidieatly
	Status()
}

type GUI_Page_Service interface {
	ChangeViewLayout()
}
