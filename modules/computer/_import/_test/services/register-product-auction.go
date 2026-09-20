/* For license and copyright information please see the LEGAL file in the code repository */

package services

import "../../libgo/achaemenid"

// RegisterProductAuctionReq is the request structure of RegisterProductAuction()
type RegisterProductAuctionReq struct {
}

// RegisterProductAuctionRes is the response structure of RegisterProductAuction()
type RegisterProductAuctionRes struct {
	ProductAuctionID [16]byte
}

// RegisterProductAuction :
func RegisterProductAuction(st *achaemenid.Stream, req *RegisterProductAuctionReq) {
}
