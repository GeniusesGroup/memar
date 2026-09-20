/* For license and copyright information please see the LEGAL file in the code repository */

package pp

import (
	"libgo/achaemenid"
	"libgo/authorization"
	"libgo/ganjine"
	"libgo/http"
	"libgo/json"
	"libgo/math"
	"libgo/price"
	"libgo/protocol"
	"libgo/service"
	"libgo/srpc"
	"libgo/syllab"
)

var updateProductPriceService = service.Service{
	URN:                "urn:giti:sabz.city:service:update-product-price",
	Domain:             DomainName,
	ID:                 13198489290766852749,
	IssueDate:          1608092793,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "",
	ExpireInFavorOfID:  0,
	Status:             protocol.Software_PreAlpha,

	Authorization: authorization.Service{
		CRUD:     authorization.CRUDUpdate,
		UserType: protocol.UserType_Org,
	},

	Name: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "Update Product Price",
	},
	Description: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "",
	},
	TAGS: []string{
		"ProductPrice",
	},

	SRPCHandler: UpdateProductPriceSRPC,
	ServeHTTP:   UpdateProductPriceHTTP,
}

// UpdateProductPriceSRPC is sRPC handler of UpdateProductPrice service.
func UpdateProductPriceSRPC(st protocol.Stream) {
	var req = &updateProductPriceReq{}
	err = req.FromSyllab(srpc.GetPayload(st.IncomePayload))
	if err != nil {
		return
	}

	err = updateProductPrice(st, req)
	// Check if any error occur in business logic
	if err != nil {
		return
	}

	st.OutcomePayload = make([]byte, srpc.MinLength)
}

// UpdateProductPriceHTTP is HTTP handler of UpdateProductPrice service.
func UpdateProductPriceHTTP(st protocol.Stream, httpReq *http.Request, httpRes *http.Response) {
	var req = &updateProductPriceReq{}
	err = req.FromJSON(httpReq.Body().Marshal())
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	err = updateProductPrice(st, req)
	// Check if any error occur in business logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
}

type updateProductPriceReq struct {
	QuiddityID [32]byte `json:",string"`

	MaterialsPercent   math.PerMyriad
	LaborPercent       math.PerMyriad
	InvestmentsPercent math.PerMyriad

	Markup math.PerMyriad
	Margin math.PerMyriad

	TaxPercent math.PerMyriad

	Price price.Amount
}

func updateProductPrice(st protocol.Stream, req *updateProductPriceReq) (err protocol.Error) {
	err = st.Authorize()
	if err != nil {
		return
	}

	var pp = data.ProductPrice{
		QuiddityID: req.QuiddityID,
	}
	err = pp.GetLastByQuiddityID()
	if err.Equal(ganjine.ErrRecordNotFound) {
		err = ErrProductPriceNotRegistered
		return
	}
	if err != nil {
		return
	}
	if pp.OrgID != st.Connection.UserID {
		err = authorization.ErrUserNotAllow
		return
	}

	pp = data.ProductPrice{
		AppInstanceID:    achaemenid.App.Nodes.LocalNode.InstanceID,
		UserConnectionID: st.Connection.ID,
		OrgID:            st.Connection.UserID,
		QuiddityID:       req.QuiddityID,

		MaterialsPercent:   req.MaterialsPercent,
		MaterialsCost:      req.Price.PerMyriad(req.MaterialsPercent),
		LaborPercent:       req.LaborPercent,
		LaborCost:          req.Price.PerMyriad(req.LaborPercent),
		InvestmentsPercent: req.InvestmentsPercent,
		InvestmentsCost:    req.Price.PerMyriad(req.InvestmentsPercent),

		Markup:          req.Markup,
		WholesaleProfit: req.Price.PerMyriad(req.Markup),
		Margin:          req.Margin,
		RetailProfit:    req.Price.PerMyriad(req.Margin),

		TaxPercent: req.TaxPercent,
		Tax:        req.Price.PerMyriad(req.TaxPercent),

		Price: req.Price,
	}
	pp.TotalCost = pp.MaterialsCost + pp.LaborCost + pp.InvestmentsCost
	err = pp.Update()
	if err != nil {
		return
	}
	return
}

/*
	Request Encoders & Decoders
*/

func (req *updateProductPriceReq) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < req.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	copy(req.QuiddityID[:], buf[0:])

	req.MaterialsPercent = math.PerMyriad(syllab.GetUInt16(buf, 32))
	req.LaborPercent = math.PerMyriad(syllab.GetUInt16(buf, 34))
	req.InvestmentsPercent = math.PerMyriad(syllab.GetUInt16(buf, 36))

	req.Markup = math.PerMyriad(syllab.GetUInt16(buf, 38))
	req.Margin = math.PerMyriad(syllab.GetUInt16(buf, 40))

	req.TaxPercent = math.PerMyriad(syllab.GetUInt16(buf, 42))

	req.Price = price.Amount(syllab.GetInt64(buf, 44))
	return
}

func (req *updateProductPriceReq) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	copy(buf[0:], req.QuiddityID[:])

	syllab.SetUInt16(buf, 32, uint16(req.MaterialsPercent))
	syllab.SetUInt16(buf, 34, uint16(req.LaborPercent))
	syllab.SetUInt16(buf, 36, uint16(req.InvestmentsPercent))

	syllab.SetUInt16(buf, 38, uint16(req.Markup))
	syllab.SetUInt16(buf, 40, uint16(req.Margin))

	syllab.SetUInt16(buf, 42, uint16(req.TaxPercent))

	syllab.SetInt64(buf, 44, int64(req.Price))
	return
}

func (req *updateProductPriceReq) LenOfSyllabStack() uint32 {
	return 52
}

func (req *updateProductPriceReq) LenOfSyllabHeap() (ln uint32) {
	return
}

func (req *updateProductPriceReq) LenAsSyllab() uint64 {
	return uint64(req.LenOfSyllabStack() + req.LenOfSyllabHeap())
}

func (req *updateProductPriceReq) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "QuiddityID":
			err = decoder.DecodeByteArrayAsBase64(req.QuiddityID[:])

		case "MaterialsPercent":
			var num uint16
			num, err = decoder.DecodeUInt16()
			req.MaterialsPercent = math.PerMyriad(num)
		case "LaborPercent":
			var num uint16
			num, err = decoder.DecodeUInt16()
			req.LaborPercent = math.PerMyriad(num)
		case "InvestmentsPercent":
			var num uint16
			num, err = decoder.DecodeUInt16()
			req.InvestmentsPercent = math.PerMyriad(num)

		case "Markup":
			var num uint16
			num, err = decoder.DecodeUInt16()
			req.Markup = math.PerMyriad(num)
		case "Margin":
			var num uint16
			num, err = decoder.DecodeUInt16()
			req.Margin = math.PerMyriad(num)

		case "TaxPercent":
			var num uint16
			num, err = decoder.DecodeUInt16()
			req.TaxPercent = math.PerMyriad(num)

		case "Price":
			var num int64
			num, err = decoder.DecodeInt64()
			req.Price = price.Amount(num)
		default:
			err = decoder.NotFoundKeyStrict()
		}

		if decoder.End() {
			return
		}
	}
	return
}

func (req *updateProductPriceReq) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	encoder.EncodeString(`{"QuiddityID":"`)
	encoder.EncodeByteSliceAsBase64(req.QuiddityID[:])

	encoder.EncodeString(`","MaterialsPercent":`)
	encoder.EncodeUInt16(uint16(req.MaterialsPercent))
	encoder.EncodeString(`,"LaborPercent":`)
	encoder.EncodeUInt16(uint16(req.LaborPercent))
	encoder.EncodeString(`,"InvestmentsPercent":`)
	encoder.EncodeUInt16(uint16(req.InvestmentsPercent))

	encoder.EncodeString(`,"Markup":`)
	encoder.EncodeUInt16(uint16(req.Markup))
	encoder.EncodeString(`,"Margin":`)
	encoder.EncodeUInt16(uint16(req.Margin))

	encoder.EncodeString(`,"TaxPercent":`)
	encoder.EncodeUInt16(uint16(req.TaxPercent))

	encoder.EncodeString(`,"Price":`)
	encoder.EncodeInt64(int64(req.Price))
	encoder.EncodeByte('}')
	return encoder.Buf
}

func (req *updateProductPriceReq) LenAsJSON() (ln int) {
	ln = 251
	return
}
