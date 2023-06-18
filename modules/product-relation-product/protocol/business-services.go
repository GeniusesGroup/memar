/* For license and copyright information please see the LEGAL file in the code repository */

package prpp

// 	FIND_ProductIDs_BY_RelationID_AND_Type(relationID pp.ProductUUID, t QuiddityRelationTypeUUID, offset, limit uint64) (productIDs []pp.ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)

type mealDeal struct {
	products []struct {
		productID string
		maxNum    int
	}
	categories []struct {
		categoryID string
		maxNum     int
	}
}
