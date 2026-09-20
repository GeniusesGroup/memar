/* For license and copyright information please see the LEGAL file in the code repository */

package services

import (
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
	"libgo/uuid"
	"libgo/validators"
)

var registerDefaultProductAuctionService = service.Service{
	URN:                "urn:giti:sabz.city:service:register-default-product-auction",
	Domain:             DomainName,
	ID:                 3858219803334193873,
	IssueDate:          1605189667,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "",
	ExpireInFavorOfID:  0,
	Status:             protocol.Software_PreAlpha,

	Authorization: authorization.Service{
		CRUD:     authorization.CRUDCreate,
		UserType: protocol.UserType_Org,
	},

	Name: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "Register Default Product Auction",
	},
	Description: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "",
	},
	TAGS: []string{
		"ProductAuction",
	},

	SRPCHandler: RegisterDefaultProductAuctionSRPC,
	ServeHTTP:   RegisterDefaultProductAuctionHTTP,
}

// RegisterDefaultProductAuctionSRPC is sRPC handler of RegisterDefaultProductAuction service.
func RegisterDefaultProductAuctionSRPC(st protocol.Stream) {
	var req = &registerDefaultProductAuctionReq{}
	err = req.FromSyllab(srpc.GetPayload(st.IncomePayload))
	if err != nil {
		return
	}

	var res *registerDefaultProductAuctionRes
	res, err = registerDefaultProductAuction(st, req)
	// Check if any error occur in business logic
	if err != nil {
		return
	}

	st.OutcomePayload = make([]byte, srpc.MinLength+res.LenAsSyllab())
	res.ToSyllab(srpc.GetPayload(st.OutcomePayload))
}

// RegisterDefaultProductAuctionHTTP is HTTP handler of RegisterDefaultProductAuction service.
func RegisterDefaultProductAuctionHTTP(st protocol.Stream, httpReq *http.Request, httpRes *http.Response) {
	var req = &registerDefaultProductAuctionReq{}
	err = req.FromJSON(httpReq.Body().Marshal())
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	var res *registerDefaultProductAuctionRes
	res, err = registerDefaultProductAuction(st, req)
	// Check if any error occur in business logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
	httpRes.SetBody(json.NewCodec(res))
}

type registerDefaultProductAuctionReq struct {
	QuiddityID [32]byte          `json:",string"`
	Language   protocol.Language // Just use to check quiddity exist and belong to requested org

	Discount                     math.PerMyriad
	DistributionCenterCommission math.PerMyriad
	SellerCommission             math.PerMyriad

	Description string `valid:"text[0:50]"`
	Type        data.ProductAuctionType
}

type registerDefaultProductAuctionRes struct {
	ID [32]byte `json:",string"`
}

func registerDefaultProductAuction(st protocol.Stream, req *registerDefaultProductAuctionReq) (res *registerDefaultProductAuctionRes, err protocol.Error) {
	err = st.Authorize()
	if err != nil {
		return
	}

	// Validate data here due to service use internally by other services!
	err = req.validator()
	if err != nil {
		return
	}

	// Check quiddity exits and belong to this Org
	var getQuiddityReq = getQuiddityReq{
		ID:       req.QuiddityID,
		Language: req.Language,
	}
	var getQuiddityRes *getQuiddityRes
	getQuiddityRes, err = getQuiddity(st, &getQuiddityReq)
	if err != nil {
		return
	}
	if getQuiddityRes.OrgID != st.Connection.UserID {
		err = authorization.ErrUserNotAllow
		return
	}
	if getQuiddityRes.Status == data.QuiddityStatusBlocked {
		err = ErrBlockedByJustice
		return
	}

	var pa = data.ProductAuction{
		QuiddityID: req.QuiddityID,
	}
	var IDs [][32]byte
	IDs, err = pa.FindIDsByQuiddityID(0, 1)
	if err.Equal(ganjine.ErrRecordNotFound) {
		err = nil
	}
	if err != nil {
		return
	}
	if len(IDs) == 1 {
		err = ErrProductAuctionRegistered
		return
	}

	pa = data.ProductAuction{
		AppInstanceID:    achaemenid.App.Nodes.LocalNode.InstanceID,
		UserConnectionID: st.Connection.ID,
		OrgID:            st.Connection.UserID,
		ID:               uuid.Random32Byte(),
		QuiddityID:       req.QuiddityID,

		Discount:         req.Discount,
		DCCommission:     req.DistributionCenterCommission,
		SellerCommission: req.SellerCommission,

		Description: req.Description,
		Type:        req.Type,
		Status:      data.ProductAuctionRegistered,
	}
	pa.Authorization.GiveFullAccess()
	err = pa.SaveNew()
	if err != nil {
		return
	}

	res = &registerDefaultProductAuctionRes{
		ID: pa.ID,
	}

	return
}

func (req *registerDefaultProductAuctionReq) validator() (err protocol.Error) {
	err = validators.ValidateText(req.Description, 0, 50)
	return
}

/*
	Request Encoders & Decoders
*/

func (req *registerDefaultProductAuctionReq) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < req.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	copy(req.QuiddityID[:], buf[0:])
	req.Language = protocol.Language(syllab.GetUInt32(buf, 32))

	req.Discount = math.PerMyriad(syllab.GetUInt16(buf, 36))
	req.DistributionCenterCommission = math.PerMyriad(syllab.GetUInt16(buf, 38))
	req.SellerCommission = math.PerMyriad(syllab.GetUInt16(buf, 40))

	req.Description = syllab.UnsafeGetString(buf, 42)
	req.Type = data.ProductAuctionType(syllab.GetUInt8(buf, 50))
	return
}

func (req *registerDefaultProductAuctionReq) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	copy(buf[0:], req.QuiddityID[:])
	syllab.SetUInt32(buf, 32, uint32(req.Language))

	syllab.SetUInt16(buf, 36, uint16(req.Discount))
	syllab.SetUInt16(buf, 38, uint16(req.DistributionCenterCommission))
	syllab.SetUInt16(buf, 40, uint16(req.SellerCommission))

	syllab.SetString(buf, req.Description, 42, heapIndex)
	syllab.SetUInt8(buf, 50, uint8(req.Type))
	return
}

func (req *registerDefaultProductAuctionReq) LenOfSyllabStack() uint32 {
	return 51
}

func (req *registerDefaultProductAuctionReq) LenOfSyllabHeap() (ln uint32) {
	ln = uint32(len(req.Description))
	return
}

func (req *registerDefaultProductAuctionReq) LenAsSyllab() uint64 {
	return uint64(req.LenOfSyllabStack() + req.LenOfSyllabHeap())
}

func (req *registerDefaultProductAuctionReq) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "QuiddityID":
			err = decoder.DecodeByteArrayAsBase64(req.QuiddityID[:])
		case "Language":
			var num uint32
			num, err = decoder.DecodeUInt32()
			req.Language = protocol.Language(num)

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

func (req *registerDefaultProductAuctionReq) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	encoder.EncodeString(`{"QuiddityID":"`)
	encoder.EncodeByteSliceAsBase64(req.QuiddityID[:])
	encoder.EncodeString(`","Language":`)
	encoder.EncodeUInt32(uint32(req.Language))

	encoder.EncodeString(`,"Discount":`)
	encoder.EncodeUInt16(uint16(req.Discount))
	encoder.EncodeString(`,"DistributionCenterCommission":`)
	encoder.EncodeUInt16(uint16(req.DistributionCenterCommission))
	encoder.EncodeString(`,"SellerCommission":`)
	encoder.EncodeUInt16(uint16(req.SellerCommission))

	encoder.EncodeString(`,"Description":"`)
	encoder.EncodeString(req.Description)
	encoder.EncodeString(`","Type":`)
	encoder.EncodeUInt8(uint8(req.Type))

	encoder.EncodeByte('}')
	return encoder.Buf
}

func (req *registerDefaultProductAuctionReq) LenAsJSON() (ln int) {
	ln = len(req.Description)
	ln += 185
	return
}

/*
	Response Encoders & Decoders
*/

func (res *registerDefaultProductAuctionRes) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < res.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	copy(res.ID[:], buf[0:])
	return
}

func (res *registerDefaultProductAuctionRes) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	copy(buf[0:], res.ID[:])
	return
}

func (res *registerDefaultProductAuctionRes) LenOfSyllabStack() uint32 {
	return 32
}

func (res *registerDefaultProductAuctionRes) LenOfSyllabHeap() (ln uint32) {
	return
}

func (res *registerDefaultProductAuctionRes) LenAsSyllab() uint64 {
	return uint64(res.LenOfSyllabStack() + res.LenOfSyllabHeap())
}

func (res *registerDefaultProductAuctionRes) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "ID":
			err = decoder.DecodeByteArrayAsBase64(res.ID[:])
		default:
			err = decoder.NotFoundKeyStrict()
		}

		if decoder.End() {
			return
		}
	}
	return
}

func (res *registerDefaultProductAuctionRes) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	encoder.EncodeString(`{"ID":"`)
	encoder.EncodeByteSliceAsBase64(res.ID[:])

	encoder.EncodeString(`"}`)
	return encoder.Buf
}

func (res *registerDefaultProductAuctionRes) LenAsJSON() (ln int) {
	ln = 52
	return
}
