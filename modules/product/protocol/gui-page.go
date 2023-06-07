/* For license and copyright information please see the LEGAL file in the code repository */

package pp

// /product?new
// /product?pid=ppppp
// /product/new

type GUI_Page_Conditions interface {
	ProductID() ProductUUID //
}

type GUI_Page_Service interface {
}
