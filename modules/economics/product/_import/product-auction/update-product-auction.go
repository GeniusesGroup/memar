/* For license and copyright information please see the LEGAL file in the code repository */

package services

import (
	"time"

	"libgo/achaemenid"
	"libgo/authorization"
	"libgo/ganjine"
	"libgo/http"
	"libgo/json"
	"libgo/math"
	"libgo/protocol"
	"libgo/service"
	"libgo/srpc"
	"libgo/syllab"
	"libgo/validators"
)

var updateProductAuctionService = service.Service{
	URN:                "urn:giti:sabz.city:service:update-product-auction",
	Domain:             DomainName,
	ID:                 4798905242890755065,
	IssueDate:          1605250043,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "",
	ExpireInFavorOfID:  0,
	Status:             protocol.Software_PreAlpha,

	Authorization: authorization.Service{
		CRUD:     authorization.CRUDUpdate,
		UserType: protocol.UserType_Org,
	},

	Name: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "Update Product Auction",
	},
	Description: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "",
	},
	TAGS: []string{
		"ProductAuction",
	},

	SRPCHandler: UpdateProductAuctionSRPC,
	ServeHTTP:   UpdateProductAuctionHTTP,
}

// UpdateProductAuctionSRPC is sRPC handler of UpdateProductAuction service.
func UpdateProductAuctionSRPC(st protocol.Stream) {
	var req = &updateProductAuctionReq{}
	err = req.FromSyllab(srpc.GetPayload(st.IncomePayload))
	if err != nil {
		return
	}

	err = updateProductAuction(st, req)
	st.OutcomePayload = make([]byte, srpc.MinLength)
}

// UpdateProductAuctionHTTP is HTTP handler of UpdateProductAuction service.
func UpdateProductAuctionHTTP(st protocol.Stream, httpReq *http.Request, httpRes *http.Response) {
	var req = &updateProductAuctionReq{}
	err = req.FromJSON(httpReq.Body().Marshal())
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	err = updateProductAuction(st, req)
	// Check if any error occur in business logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
}

type updateProductAuctionReq struct {
	ID [32]byte `json:",string"`

	// Price
	Discount                     math.PerMyriad
	DistributionCenterCommission math.PerMyriad
	SellerCommission             math.PerMyriad

	// Authorization
	Authorization authorization.Product

	Description string `valid:"text[0:50]"`
	Type        data.ProductAuctionType
}

func updateProductAuction(st protocol.Stream, req *updateProductAuctionReq) (err protocol.Error) {
	err = st.Authorize()
	if err != nil {
		return
	}

	var pa = data.ProductAuction{
		ID: req.ID,
	}
	err = pa.GetLastByID()
	if err.Equal(ganjine.ErrRecordNotFound) {
		err = ErrProductAuctionNotRegistered
		return
	}
	if err != nil {
		return
	}
	if pa.OrgID != st.Connection.UserID {
		err = authorization.ErrUserNotAllow
		return
	}
	if pa.Status == data.QuiddityStatusBlocked {
		err = ErrBlockedByJustice
		return
	}

	pa = data.ProductAuction{
		AppInstanceID:    achaemenid.App.Nodes.LocalNode.InstanceID,
		UserConnectionID: st.Connection.ID,
		OrgID:            pa.OrgID,
		ID:               pa.ID,
		QuiddityID:       pa.QuiddityID,

		Discount:         req.Discount,
		DCCommission:     req.DistributionCenterCommission,
		SellerCommission: req.SellerCommission,

		// Authorization
		Authorization: req.Authorization,

		Description: req.Description,
		Type:        req.Type,
		Status:      data.ProductAuctionUpdated,
	}

	if req.Authorization.LiveUntil != 0 && req.Authorization.LiveUntil.Pass(time.Now()) {
		pa.Status = data.ProductAuctionExpired
	}

	err = pa.Set()
	if err != nil {
		return
	}
	pa.IndexRecordIDForID()
	return
}

func (req *updateProductAuctionReq) validator() (err protocol.Error) {
	err = validators.ValidateText(req.Description, 0, 50)
	return
}

/*
	Request Encoders & Decoders
*/

func (req *updateProductAuctionReq) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < req.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	copy(req.ID[:], buf[0:])

	req.Discount = math.PerMyriad(syllab.GetUInt16(buf, 32))
	req.DistributionCenterCommission = math.PerMyriad(syllab.GetUInt16(buf, 34))
	req.SellerCommission = math.PerMyriad(syllab.GetUInt16(buf, 36))

	req.Authorization.FromSyllab(buf, 38)

	req.Description = syllab.UnsafeGetString(buf, 38+req.Authorization.LenOfSyllabStack())
	req.Type = data.ProductAuctionType(syllab.GetUInt8(buf, 46+req.Authorization.LenOfSyllabStack()))
	return
}

func (req *updateProductAuctionReq) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	copy(buf[0:], req.ID[:])

	syllab.SetUInt16(buf, 32, uint16(req.Discount))
	syllab.SetUInt16(buf, 34, uint16(req.DistributionCenterCommission))
	syllab.SetUInt16(buf, 36, uint16(req.SellerCommission))

	req.Authorization.ToSyllab(buf, 38)

	heapIndex = syllab.SetString(buf, req.Description, 38+req.Authorization.LenOfSyllabStack(), heapIndex)
	syllab.SetUInt8(buf, 46+req.Authorization.LenOfSyllabStack(), uint8(req.Type))
	return
}

func (req *updateProductAuctionReq) LenOfSyllabStack() uint32 {
	return 47 + req.Authorization.LenOfSyllabStack()
}

func (req *updateProductAuctionReq) LenOfSyllabHeap() (ln uint32) {
	ln += req.Authorization.LenOfSyllabHeap()
	ln += uint32(len(req.Description))
	return
}

func (req *updateProductAuctionReq) LenAsSyllab() uint64 {
	return uint64(req.LenOfSyllabStack() + req.LenOfSyllabHeap())
}

func (req *updateProductAuctionReq) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "ID":
			err = decoder.DecodeByteArrayAsBase64(req.ID[:])

		case "Discount":
			var num uint16
			num, err = decoder.DecodeUInt16()
			req.Discount = math.PerMyriad(num)
		case "DistributionCenterCommission":
			var num uint16
			num, err = decoder.DecodeUInt16()
			req.DistributionCenterCommission = math.PerMyriad(num)
		case "SellerCommission":
			var num uint16
			num, err = decoder.DecodeUInt16()
			req.SellerCommission = math.PerMyriad(num)

		case "Authorization":
			err = req.Authorization.JSONDecoder(&decoder)

		case "Description":
			req.Description, err = decoder.DecodeString()
		case "Type":
			var num uint8
			num, err = decoder.DecodeUInt8()
			req.Type = data.ProductAuctionType(num)
		default:
			err = decoder.NotFoundKeyStrict()
		}

		if decoder.End() {
			return
		}
	}
	return
}

func (req *updateProductAuctionReq) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}
	encoder.EncodeString(`{"ID":"`)
	encoder.EncodeByteSliceAsBase64(req.ID[:])
	encoder.EncodeString(`","Discount":`)
	encoder.EncodeUInt16(uint16(req.Discount))
	encoder.EncodeString(`,"DistributionCenterCommission":`)
	encoder.EncodeUInt16(uint16(req.DistributionCenterCommission))
	encoder.EncodeString(`,"SellerCommission":`)
	encoder.EncodeUInt16(uint16(req.SellerCommission))
	encoder.EncodeString(`,"Authorization":`)
	req.Authorization.JSONEncoder(&encoder)
	encoder.EncodeString(`,"Description":"`)
	encoder.EncodeString(req.Description)
	encoder.EncodeString(`","Type":`)
	encoder.EncodeUInt8(uint8(req.Type))
	encoder.EncodeByte('}')
	return encoder.Buf
}

func (req *updateProductAuctionReq) LenAsJSON() (ln int) {
	ln = len(req.Description)
	ln += req.Authorization.LenAsJSON()
	ln += 179
	return
}
