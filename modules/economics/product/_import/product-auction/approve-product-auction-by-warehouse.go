/* For license and copyright information please see the LEGAL file in the code repository */

package services

import "libgo/achaemenid"

var approveProductAuctionByWarehouseService = achaemenid.Service{
	ID:                0,
	Name:              "approveProductAuctionByWarehouse",
	IssueDate:         0,
	ExpiryDate:        0,
	ExpireInFavorOf:   "",
	ExpireInFavorOfID: 0,
	Status:            achaemenid.ServiceStatePreAlpha,
	Handler:           ApproveProductAuctionByWarehouse,
	Description: []string{
		``,
	},
	TAGS: []string{"Product"},
}

// ApproveProductAuctionByWarehouse will
func ApproveProductAuctionByWarehouse(s *achaemenid.Server, st *achaemenid.Stream) {}

func approveProductAuctionByWarehouse(st *achaemenid.Stream, req *approveProductAuctionByWarehouseReq) {

	// Authorization : Just related org can send request and approve their items, not user invoice owner.

	// If warehouse can not approve some items, set to zero number.

	// If logisticType set to OnUserPlace we must make needed services for transport
	// Set invoiceID for transport in Logistic:Delivery

	// change items logistic status
	// We must tell related service about to continue process.

	// Write data to Database
	// st.Err = usersdata.UpdateData(&dbRequest)
}

type approveProductAuctionByWarehouseReq struct {
	ProductAuction [16]string
}
