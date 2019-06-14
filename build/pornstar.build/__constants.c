
#include "nuitka/prelude.h"
#include "structseq.h"

// Sentinel PyObject to be used for all our call iterator endings. It will
// become a PyCObject pointing to NULL. It's address is unique, and that's
// enough for us to use it as sentinel value.
PyObject *_sentinel_value = NULL;

PyObject *Nuitka_dunder_compiled_value = NULL;

PyObject *const_int_0;
PyObject *const_str_dot;
PyObject *const_float_0_0;
PyObject *const_float_0_3;
PyObject *const_float_0_5;
PyObject *const_float_0_7;
PyObject *const_float_0_9;
PyObject *const_float_1_0;
PyObject *const_int_neg_1;
PyObject *const_int_pos_1;
PyObject *const_int_pos_2;
PyObject *const_int_pos_3;
PyObject *const_int_pos_4;
PyObject *const_int_pos_7;
PyObject *const_str_empty;
PyObject *const_dict_empty;
PyObject *const_int_pos_12;
PyObject *const_int_pos_64;
PyObject *const_bytes_empty;
PyObject *const_float_0_001;
PyObject *const_int_pos_100;
PyObject *const_int_pos_128;
PyObject *const_int_pos_256;
PyObject *const_int_pos_500;
PyObject *const_int_pos_512;
PyObject *const_str_plain_a;
PyObject *const_str_plain_c;
PyObject *const_str_plain_f;
PyObject *const_str_plain_h;
PyObject *const_str_plain_i;
PyObject *const_str_plain_m;
PyObject *const_str_plain_n;
PyObject *const_str_plain_o;
PyObject *const_str_plain_r;
PyObject *const_str_plain_t;
PyObject *const_str_plain_w;
PyObject *const_str_plain_x;
PyObject *const_str_plain_y;
PyObject *const_tuple_empty;
PyObject *const_int_pos_1024;
PyObject *const_str_plain_id;
PyObject *const_str_plain_np;
PyObject *const_str_plain_os;
PyObject *const_str_plain_rb;
PyObject *const_str_plain_tf;
PyObject *const_str_plain_wb;
PyObject *const_str_plain_x1;
PyObject *const_str_plain_x2;
PyObject *const_str_plain_y1;
PyObject *const_str_plain_y2;
PyObject *const_str_plain_all;
PyObject *const_str_plain_any;
PyObject *const_str_plain_end;
PyObject *const_str_plain_exp;
PyObject *const_str_plain_get;
PyObject *const_str_plain_ixs;
PyObject *const_str_plain_log;
PyObject *const_str_plain_max;
PyObject *const_str_plain_min;
PyObject *const_str_plain_out;
PyObject *const_str_plain_pad;
PyObject *const_str_plain_sum;
PyObject *const_str_plain_sys;
PyObject *const_str_plain_zip;
PyObject *const_list_none_list;
PyObject *const_str_plain_NAME;
PyObject *const_str_plain_None;
PyObject *const_str_plain_axis;
PyObject *const_str_plain_bbox;
PyObject *const_str_plain_bool;
PyObject *const_str_plain_cast;
PyObject *const_str_plain_crop;
PyObject *const_str_plain_dict;
PyObject *const_str_plain_file;
PyObject *const_str_plain_info;
PyObject *const_str_plain_join;
PyObject *const_str_plain_keys;
PyObject *const_str_plain_list;
PyObject *const_str_plain_logs;
PyObject *const_str_plain_mask;
PyObject *const_str_plain_math;
PyObject *const_str_plain_mean;
PyObject *const_str_plain_mode;
PyObject *const_str_plain_name;
PyObject *const_str_plain_ones;
PyObject *const_str_plain_open;
PyObject *const_str_plain_path;
PyObject *const_str_plain_read;
PyObject *const_str_plain_resp;
PyObject *const_str_plain_rois;
PyObject *const_str_plain_self;
PyObject *const_str_plain_send;
PyObject *const_str_plain_size;
PyObject *const_str_plain_sqrt;
PyObject *const_str_plain_type;
PyObject *const_str_plain_False;
PyObject *const_str_plain_array;
PyObject *const_str_plain_boxes;
PyObject *const_str_plain_bytes;
PyObject *const_str_plain_close;
PyObject *const_str_plain_dtype;
PyObject *const_str_plain_empty;
PyObject *const_str_plain_heads;
PyObject *const_str_plain_image;
PyObject *const_str_plain_int32;
PyObject *const_str_plain_level;
PyObject *const_str_plain_lower;
PyObject *const_str_plain_masks;
PyObject *const_str_plain_model;
PyObject *const_str_plain_names;
PyObject *const_str_plain_numpy;
PyObject *const_str_plain_print;
PyObject *const_str_plain_range;
PyObject *const_str_plain_round;
PyObject *const_str_plain_scale;
PyObject *const_str_plain_shape;
PyObject *const_str_plain_shift;
PyObject *const_str_plain_split;
PyObject *const_str_plain_stack;
PyObject *const_str_plain_throw;
PyObject *const_str_plain_train;
PyObject *const_str_plain_tuple;
PyObject *const_str_plain_types;
PyObject *const_str_plain_uint8;
PyObject *const_str_plain_where;
PyObject *const_str_plain_width;
PyObject *const_str_plain_zeros;
PyObject *const_str_plain_Config;
PyObject *const_str_plain_Fliplr;
PyObject *const_str_plain_append;
PyObject *const_str_plain_arange;
PyObject *const_str_plain_argmax;
PyObject *const_str_plain_around;
PyObject *const_str_plain_astype;
PyObject *const_str_plain_config;
PyObject *const_str_plain_counts;
PyObject *const_str_plain_delete;
PyObject *const_str_plain_deltas;
PyObject *const_str_plain_detect;
PyObject *const_str_plain_divide;
PyObject *const_str_plain_epochs;
PyObject *const_str_plain_exists;
PyObject *const_str_plain_extend;
PyObject *const_str_plain_format;
PyObject *const_str_plain_height;
PyObject *const_str_plain_images;
PyObject *const_str_plain_imgaug;
PyObject *const_str_plain_inputs;
PyObject *const_str_plain_kwargs;
PyObject *const_str_plain_layers;
PyObject *const_str_plain_locals;
PyObject *const_str_plain_object;
PyObject *const_str_plain_origin;
PyObject *const_str_plain_random;
PyObject *const_str_plain_resize;
PyObject *const_str_plain_result;
PyObject *const_str_plain_scores;
PyObject *const_str_plain_shutil;
PyObject *const_str_plain_sorted;
PyObject *const_str_plain_source;
PyObject *const_str_plain_square;
PyObject *const_str_plain_urllib;
PyObject *const_tuple_none_tuple;
PyObject *const_str_plain_Dataset;
PyObject *const_str_plain___all__;
PyObject *const_str_plain___cmp__;
PyObject *const_str_plain___doc__;
PyObject *const_str_plain___model;
PyObject *const_str_plain___utils;
PyObject *const_str_plain_abspath;
PyObject *const_str_plain_anchors;
PyObject *const_str_plain_by_name;
PyObject *const_str_plain_compile;
PyObject *const_str_plain_default;
PyObject *const_str_plain_display;
PyObject *const_str_plain_float32;
PyObject *const_str_plain_globals;
PyObject *const_str_plain_indices;
PyObject *const_str_plain_inspect;
PyObject *const_str_plain_logging;
PyObject *const_str_plain_maximum;
PyObject *const_str_plain_minimum;
PyObject *const_str_plain_outputs;
PyObject *const_str_plain_padding;
PyObject *const_str_plain_prepare;
PyObject *const_str_plain_randint;
PyObject *const_str_plain_request;
PyObject *const_str_plain_reshape;
PyObject *const_str_plain_results;
PyObject *const_str_plain_urlopen;
PyObject *const_str_plain_verbose;
PyObject *const_str_plain_warning;
PyObject *const_str_angle_listcomp;
PyObject *const_str_plain_BACKBONE;
PyObject *const_str_plain_Ellipsis;
PyObject *const_str_plain_MaskRCNN;
PyObject *const_str_plain_ROOT_DIR;
PyObject *const_str_plain_TRAIN_BN;
PyObject *const_str_plain___dict__;
PyObject *const_str_plain___exit__;
PyObject *const_str_plain___file__;
PyObject *const_str_plain___init__;
PyObject *const_str_plain___iter__;
PyObject *const_str_plain___name__;
PyObject *const_str_plain___path__;
PyObject *const_str_plain___spec__;
PyObject *const_str_plain_callable;
PyObject *const_str_plain_center_x;
PyObject *const_str_plain_center_y;
PyObject *const_str_plain_class_id;
PyObject *const_str_plain_constant;
PyObject *const_str_plain_fromlist;
PyObject *const_str_plain_gt_boxes;
PyObject *const_str_plain_gt_masks;
PyObject *const_str_plain_image_id;
PyObject *const_str_plain_makedirs;
PyObject *const_str_plain_multiply;
PyObject *const_str_plain_terminal;
PyObject *const_str_plain_training;
PyObject *const_str_angle_metaclass;
PyObject *const_str_plain_GPU_COUNT;
PyObject *const_str_plain_POOL_SIZE;
PyObject *const_str_plain___class__;
PyObject *const_str_plain___debug__;
PyObject *const_str_plain___enter__;
PyObject *const_str_plain_add_class;
PyObject *const_str_plain_add_image;
PyObject *const_str_plain_bytearray;
PyObject *const_str_plain_class_ids;
PyObject *const_str_plain_class_map;
PyObject *const_str_plain_enumerate;
PyObject *const_str_plain_find_last;
PyObject *const_str_plain_image_ids;
PyObject *const_str_plain_inference;
PyObject *const_str_plain_load_mask;
PyObject *const_str_plain_metaclass;
PyObject *const_str_plain_model_dir;
PyObject *const_str_plain_resnet101;
PyObject *const_slice_none_none_none;
PyObject *const_str_plain_BATCH_SIZE;
PyObject *const_str_plain_CocoConfig;
PyObject *const_str_plain_MASK_SHAPE;
PyObject *const_str_plain_MEAN_PIXEL;
PyObject *const_str_plain___cached__;
PyObject *const_str_plain___import__;
PyObject *const_str_plain___loader__;
PyObject *const_str_plain___module__;
PyObject *const_str_plain_batch_size;
PyObject *const_str_plain_image_info;
PyObject *const_str_plain_load_image;
PyObject *const_str_plain_model_path;
PyObject *const_str_plain_norm_boxes;
PyObject *const_str_plain_pred_masks;
PyObject *const_str_plain_startswith;
PyObject *const_str_plain_tensorflow;
PyObject *const_str_plain_trim_zeros;
PyObject *const_str_plain_IMAGE_SHAPE;
PyObject *const_str_plain_NUM_CLASSES;
PyObject *const_str_plain___getitem__;
PyObject *const_str_plain___package__;
PyObject *const_str_plain___prepare__;
PyObject *const_str_plain___version__;
PyObject *const_str_plain_batch_slice;
PyObject *const_str_plain_classmethod;
PyObject *const_str_plain_compute_iou;
PyObject *const_str_plain_concatenate;
PyObject *const_str_plain_copyfileobj;
PyObject *const_str_plain_image_shape;
PyObject *const_str_plain_num_classes;
PyObject *const_str_plain_resize_mask;
PyObject *const_str_plain_unmold_mask;
PyObject *const_tuple_float_0_5_tuple;
PyObject *const_tuple_int_pos_1_tuple;
PyObject *const_tuple_type_bool_tuple;
PyObject *const_str_plain_BBOX_STD_DEV;
PyObject *const_str_plain_LOSS_WEIGHTS;
PyObject *const_str_plain_LooseVersion;
PyObject *const_str_plain_USE_RPN_ROIS;
PyObject *const_str_plain_WEIGHT_DECAY;
PyObject *const_str_plain___builtins__;
PyObject *const_str_plain___compiled__;
PyObject *const_str_plain___internal__;
PyObject *const_str_plain___qualname__;
PyObject *const_str_plain_augmentation;
PyObject *const_str_plain_denorm_boxes;
PyObject *const_str_plain_gt_class_ids;
PyObject *const_str_plain_has_location;
PyObject *const_str_plain_load_weights;
PyObject *const_str_plain_resize_image;
PyObject *const_str_plain_staticmethod;
PyObject *const_str_plain_IMAGE_MAX_DIM;
PyObject *const_str_plain_IMAGE_MIN_DIM;
PyObject *const_str_plain_LEARNING_RATE;
PyObject *const_str_plain_PRE_NMS_LIMIT;
PyObject *const_str_plain_USE_MINI_MASK;
PyObject *const_str_plain___metaclass__;
PyObject *const_str_plain__initializing;
PyObject *const_str_plain_anchor_stride;
PyObject *const_str_plain_iou_threshold;
PyObject *const_str_plain_learning_rate;
PyObject *const_str_plain_minimize_mask;
PyObject *const_str_plain_rpn_bbox_loss;
PyObject *const_tuple_int_0_int_0_tuple;
PyObject *const_tuple_str_plain_x_tuple;
PyObject *const_tuple_type_object_tuple;
PyObject *const_str_plain_IMAGES_PER_GPU;
PyObject *const_str_plain_MASK_POOL_SIZE;
PyObject *const_str_plain_box_refinement;
PyObject *const_str_plain_extract_bboxes;
PyObject *const_str_plain_pred_class_ids;
PyObject *const_str_plain_rpn_class_loss;
PyObject *const_slice_int_pos_1_none_none;
PyObject *const_slice_none_int_pos_2_none;
PyObject *const_slice_none_int_pos_4_none;
PyObject *const_slice_none_none_int_neg_1;
PyObject *const_str_plain_COCO_MODEL_PATH;
PyObject *const_str_plain_IMAGE_META_SIZE;
PyObject *const_str_plain_IMAGE_MIN_SCALE;
PyObject *const_str_plain_MINI_MASK_SHAPE;
PyObject *const_str_plain_STEPS_PER_EPOCH;
PyObject *const_str_plain_constant_values;
PyObject *const_str_plain_image_reference;
PyObject *const_str_plain_mrcnn_bbox_loss;
PyObject *const_str_plain_mrcnn_mask_loss;
PyObject *const_str_plain_BACKBONE_STRIDES;
PyObject *const_str_plain_MAX_GT_INSTANCES;
PyObject *const_str_plain_RPN_BBOX_STD_DEV;
PyObject *const_str_plain_VALIDATION_STEPS;
PyObject *const_str_plain_compute_overlaps;
PyObject *const_str_plain_mrcnn_class_loss;
PyObject *const_str_plain_source_class_ids;
PyObject *const_tuple_none_none_none_tuple;
PyObject *const_tuple_str_plain_self_tuple;
PyObject *const_str_plain_IMAGE_RESIZE_MODE;
PyObject *const_str_plain_LEARNING_MOMENTUM;
PyObject *const_str_plain_RPN_ANCHOR_RATIOS;
PyObject *const_str_plain_RPN_ANCHOR_SCALES;
PyObject *const_str_plain_RPN_ANCHOR_STRIDE;
PyObject *const_str_plain_RPN_NMS_THRESHOLD;
PyObject *const_str_plain_GRADIENT_CLIP_NORM;
PyObject *const_str_plain_ROI_POSITIVE_RATIO;
PyObject *const_str_plain_get_source_class_id;
PyObject *const_str_plain_map_source_class_id;
PyObject *const_str_plain_non_max_suppression;
PyObject *const_str_plain_TRAIN_ROIS_PER_IMAGE;
PyObject *const_str_plain_box_refinement_graph;
PyObject *const_str_plain_get_imagenet_weights;
PyObject *const_tuple_str_plain_MaskRCNN_tuple;
PyObject *const_str_plain_TOP_DOWN_PYRAMID_SIZE;
PyObject *const_tuple_str_plain___class___tuple;
PyObject *const_str_plain_COMPUTE_BACKBONE_SHAPE;
PyObject *const_str_plain_POST_NMS_ROIS_TRAINING;
PyObject *const_str_plain_DETECTION_MAX_INSTANCES;
PyObject *const_str_plain_DETECTION_NMS_THRESHOLD;
PyObject *const_str_plain_POST_NMS_ROIS_INFERENCE;
PyObject *const_str_plain_DETECTION_MIN_CONFIDENCE;
PyObject *const_str_plain_download_trained_weights;
PyObject *const_str_plain_generate_pyramid_anchors;
PyObject *const_tuple_str_plain_LooseVersion_tuple;
PyObject *const_tuple_str_plain_o_str_plain_n_tuple;
PyObject *const_str_plain_FPN_CLASSIF_FC_LAYERS_SIZE;
PyObject *const_str_plain_submodule_search_locations;
PyObject *const_dict_54f4aa72cf3f950a22814f798a2888e8;
PyObject *const_dict_72c7b31d39de2eb4cb1f11a06c118ebc;
PyObject *const_dict_8a6ce79bb59f45c062c2a0027a3a0c33;
PyObject *const_dict_9e8fa581e6a44c6d65a10c615ae35aa0;
PyObject *const_dict_a706c749f33afbbf180a37810efcd0ba;
PyObject *const_dict_c4b01644824ba6bad132707fcdaa03f1;
PyObject *const_str_plain_RPN_TRAIN_ANCHORS_PER_IMAGE;
PyObject *const_tuple_slice_none_none_none_int_0_tuple;
PyObject *const_list_int_0_int_0_int_pos_1_int_pos_1_list;
PyObject *const_tuple_slice_none_none_none_int_pos_1_tuple;
PyObject *const_tuple_slice_none_none_none_int_pos_2_tuple;
PyObject *const_tuple_slice_none_none_none_int_pos_3_tuple;
PyObject *const_str_digest_067240ca281436a921966038f28af45c;
PyObject *const_str_digest_22e74f88adcfbcd2c9bec40d576e19a9;
PyObject *const_str_digest_25731c733fd74e8333aa29126ce85686;
PyObject *const_str_digest_45e4dde2057b0bf276d6a84f4c917d27;
PyObject *const_str_digest_4a0edff902aeaeff9fce1ee73187e8e1;
PyObject *const_str_digest_4af59da437d2f21ccb08423e5fb98074;
PyObject *const_str_digest_59bc9c95777e64e4720c3af0837aec42;
PyObject *const_str_digest_75fd71b1edada749c2ef7ac810062295;
PyObject *const_str_digest_9816e8d1552296af90d250823c964059;
PyObject *const_str_digest_adc474dd61fbd736d69c1bac5d9712e0;
PyObject *const_tuple_b709b748889c3a3b2974dc8135f76387_tuple;
PyObject *const_str_plain_get_human_and_background_from_a_frame;
PyObject *const_tuple_anon_function_anon_builtin_function_or_method_tuple;

static void _createGlobalConstants( void )
{
    NUITKA_MAY_BE_UNUSED PyObject *exception_type, *exception_value;
    NUITKA_MAY_BE_UNUSED PyTracebackObject *exception_tb;

#ifdef _MSC_VER
    // Prevent unused warnings in case of simple programs, the attribute
    // NUITKA_MAY_BE_UNUSED doesn't work for MSVC.
    (void *)exception_type; (void *)exception_value; (void *)exception_tb;
#endif

    const_int_0 = PyLong_FromUnsignedLong( 0ul );
    const_str_dot = UNSTREAM_STRING_ASCII( &constant_bin[ 62 ], 1, 0 );
    const_float_0_0 = UNSTREAM_FLOAT( &constant_bin[ 55384 ] );
    const_float_0_3 = UNSTREAM_FLOAT( &constant_bin[ 55392 ] );
    const_float_0_5 = UNSTREAM_FLOAT( &constant_bin[ 55400 ] );
    const_float_0_7 = UNSTREAM_FLOAT( &constant_bin[ 55408 ] );
    const_float_0_9 = UNSTREAM_FLOAT( &constant_bin[ 55416 ] );
    const_float_1_0 = UNSTREAM_FLOAT( &constant_bin[ 55424 ] );
    const_int_neg_1 = PyLong_FromLong( -1l );
    const_int_pos_1 = PyLong_FromUnsignedLong( 1ul );
    const_int_pos_2 = PyLong_FromUnsignedLong( 2ul );
    const_int_pos_3 = PyLong_FromUnsignedLong( 3ul );
    const_int_pos_4 = PyLong_FromUnsignedLong( 4ul );
    const_int_pos_7 = PyLong_FromUnsignedLong( 7ul );
    const_str_empty = UNSTREAM_STRING_ASCII( &constant_bin[ 0 ], 0, 0 );
    const_dict_empty = _PyDict_NewPresized( 0 );
    assert( PyDict_Size( const_dict_empty ) == 0 );
    const_int_pos_12 = PyLong_FromUnsignedLong( 12ul );
    const_int_pos_64 = PyLong_FromUnsignedLong( 64ul );
    const_bytes_empty = UNSTREAM_BYTES( &constant_bin[ 0 ], 0 );
    const_float_0_001 = UNSTREAM_FLOAT( &constant_bin[ 55432 ] );
    const_int_pos_100 = PyLong_FromUnsignedLong( 100ul );
    const_int_pos_128 = PyLong_FromUnsignedLong( 128ul );
    const_int_pos_256 = PyLong_FromUnsignedLong( 256ul );
    const_int_pos_500 = PyLong_FromUnsignedLong( 500ul );
    const_int_pos_512 = PyLong_FromUnsignedLong( 512ul );
    const_str_plain_a = UNSTREAM_STRING_ASCII( &constant_bin[ 10 ], 1, 1 );
    const_str_plain_c = UNSTREAM_STRING_ASCII( &constant_bin[ 104 ], 1, 1 );
    const_str_plain_f = UNSTREAM_STRING_ASCII( &constant_bin[ 332 ], 1, 1 );
    const_str_plain_h = UNSTREAM_STRING_ASCII( &constant_bin[ 138 ], 1, 1 );
    const_str_plain_i = UNSTREAM_STRING_ASCII( &constant_bin[ 3 ], 1, 1 );
    const_str_plain_m = UNSTREAM_STRING_ASCII( &constant_bin[ 9 ], 1, 1 );
    const_str_plain_n = UNSTREAM_STRING_ASCII( &constant_bin[ 1 ], 1, 1 );
    const_str_plain_o = UNSTREAM_STRING_ASCII( &constant_bin[ 5 ], 1, 1 );
    const_str_plain_r = UNSTREAM_STRING_ASCII( &constant_bin[ 4 ], 1, 1 );
    const_str_plain_t = UNSTREAM_STRING_ASCII( &constant_bin[ 33 ], 1, 1 );
    const_str_plain_w = UNSTREAM_STRING_ASCII( &constant_bin[ 462 ], 1, 1 );
    const_str_plain_x = UNSTREAM_STRING_ASCII( &constant_bin[ 41 ], 1, 1 );
    const_str_plain_y = UNSTREAM_STRING_ASCII( &constant_bin[ 64 ], 1, 1 );
    const_tuple_empty = PyTuple_New( 0 );
    const_int_pos_1024 = PyLong_FromUnsignedLong( 1024ul );
    const_str_plain_id = UNSTREAM_STRING_ASCII( &constant_bin[ 354 ], 2, 1 );
    const_str_plain_np = UNSTREAM_STRING_ASCII( &constant_bin[ 7725 ], 2, 1 );
    const_str_plain_os = UNSTREAM_STRING_ASCII( &constant_bin[ 7658 ], 2, 1 );
    const_str_plain_rb = UNSTREAM_STRING_ASCII( &constant_bin[ 43966 ], 2, 1 );
    const_str_plain_tf = UNSTREAM_STRING_ASCII( &constant_bin[ 7863 ], 2, 1 );
    const_str_plain_wb = UNSTREAM_STRING_ASCII( &constant_bin[ 6760 ], 2, 1 );
    const_str_plain_x1 = UNSTREAM_STRING_ASCII( &constant_bin[ 7662 ], 2, 1 );
    const_str_plain_x2 = UNSTREAM_STRING_ASCII( &constant_bin[ 7285 ], 2, 1 );
    const_str_plain_y1 = UNSTREAM_STRING_ASCII( &constant_bin[ 8602 ], 2, 1 );
    const_str_plain_y2 = UNSTREAM_STRING_ASCII( &constant_bin[ 8610 ], 2, 1 );
    const_str_plain_all = UNSTREAM_STRING_ASCII( &constant_bin[ 3029 ], 3, 1 );
    const_str_plain_any = UNSTREAM_STRING_ASCII( &constant_bin[ 28587 ], 3, 1 );
    const_str_plain_end = UNSTREAM_STRING_ASCII( &constant_bin[ 12764 ], 3, 1 );
    const_str_plain_exp = UNSTREAM_STRING_ASCII( &constant_bin[ 3323 ], 3, 1 );
    const_str_plain_get = UNSTREAM_STRING_ASCII( &constant_bin[ 4767 ], 3, 1 );
    const_str_plain_ixs = UNSTREAM_STRING_ASCII( &constant_bin[ 45746 ], 3, 1 );
    const_str_plain_log = UNSTREAM_STRING_ASCII( &constant_bin[ 143 ], 3, 1 );
    const_str_plain_max = UNSTREAM_STRING_ASCII( &constant_bin[ 7229 ], 3, 1 );
    const_str_plain_min = UNSTREAM_STRING_ASCII( &constant_bin[ 363 ], 3, 1 );
    const_str_plain_out = UNSTREAM_STRING_ASCII( &constant_bin[ 7554 ], 3, 1 );
    const_str_plain_pad = UNSTREAM_STRING_ASCII( &constant_bin[ 9088 ], 3, 1 );
    const_str_plain_sum = UNSTREAM_STRING_ASCII( &constant_bin[ 4747 ], 3, 1 );
    const_str_plain_sys = UNSTREAM_STRING_ASCII( &constant_bin[ 55440 ], 3, 1 );
    const_str_plain_zip = UNSTREAM_STRING_ASCII( &constant_bin[ 225 ], 3, 1 );
    const_list_none_list = PyList_New( 1 );
    PyList_SET_ITEM( const_list_none_list, 0, Py_None ); Py_INCREF( Py_None );
    const_str_plain_NAME = UNSTREAM_STRING_ASCII( &constant_bin[ 55443 ], 4, 1 );
    const_str_plain_None = UNSTREAM_STRING_ASCII( &constant_bin[ 37818 ], 4, 1 );
    const_str_plain_axis = UNSTREAM_STRING_ASCII( &constant_bin[ 43289 ], 4, 1 );
    const_str_plain_bbox = UNSTREAM_STRING_ASCII( &constant_bin[ 1572 ], 4, 1 );
    const_str_plain_bool = UNSTREAM_STRING_ASCII( &constant_bin[ 848 ], 4, 1 );
    const_str_plain_cast = UNSTREAM_STRING_ASCII( &constant_bin[ 19750 ], 4, 1 );
    const_str_plain_crop = UNSTREAM_STRING_ASCII( &constant_bin[ 9097 ], 4, 1 );
    const_str_plain_dict = UNSTREAM_STRING_ASCII( &constant_bin[ 153 ], 4, 1 );
    const_str_plain_file = UNSTREAM_STRING_ASCII( &constant_bin[ 3162 ], 4, 1 );
    const_str_plain_info = UNSTREAM_STRING_ASCII( &constant_bin[ 46264 ], 4, 1 );
    const_str_plain_join = UNSTREAM_STRING_ASCII( &constant_bin[ 55447 ], 4, 1 );
    const_str_plain_keys = UNSTREAM_STRING_ASCII( &constant_bin[ 55451 ], 4, 1 );
    const_str_plain_list = UNSTREAM_STRING_ASCII( &constant_bin[ 8529 ], 4, 1 );
    const_str_plain_logs = UNSTREAM_STRING_ASCII( &constant_bin[ 143 ], 4, 1 );
    const_str_plain_mask = UNSTREAM_STRING_ASCII( &constant_bin[ 592 ], 4, 1 );
    const_str_plain_math = UNSTREAM_STRING_ASCII( &constant_bin[ 55455 ], 4, 1 );
    const_str_plain_mean = UNSTREAM_STRING_ASCII( &constant_bin[ 32219 ], 4, 1 );
    const_str_plain_mode = UNSTREAM_STRING_ASCII( &constant_bin[ 2143 ], 4, 1 );
    const_str_plain_name = UNSTREAM_STRING_ASCII( &constant_bin[ 85 ], 4, 1 );
    const_str_plain_ones = UNSTREAM_STRING_ASCII( &constant_bin[ 55459 ], 4, 1 );
    const_str_plain_open = UNSTREAM_STRING_ASCII( &constant_bin[ 55463 ], 4, 1 );
    const_str_plain_path = UNSTREAM_STRING_ASCII( &constant_bin[ 135 ], 4, 1 );
    const_str_plain_read = UNSTREAM_STRING_ASCII( &constant_bin[ 8304 ], 4, 1 );
    const_str_plain_resp = UNSTREAM_STRING_ASCII( &constant_bin[ 25735 ], 4, 1 );
    const_str_plain_rois = UNSTREAM_STRING_ASCII( &constant_bin[ 7343 ], 4, 1 );
    const_str_plain_self = UNSTREAM_STRING_ASCII( &constant_bin[ 21197 ], 4, 1 );
    const_str_plain_send = UNSTREAM_STRING_ASCII( &constant_bin[ 55467 ], 4, 1 );
    const_str_plain_size = UNSTREAM_STRING_ASCII( &constant_bin[ 7509 ], 4, 1 );
    const_str_plain_sqrt = UNSTREAM_STRING_ASCII( &constant_bin[ 55471 ], 4, 1 );
    const_str_plain_type = UNSTREAM_STRING_ASCII( &constant_bin[ 1565 ], 4, 1 );
    const_str_plain_False = UNSTREAM_STRING_ASCII( &constant_bin[ 3115 ], 5, 1 );
    const_str_plain_array = UNSTREAM_STRING_ASCII( &constant_bin[ 853 ], 5, 1 );
    const_str_plain_boxes = UNSTREAM_STRING_ASCII( &constant_bin[ 8638 ], 5, 1 );
    const_str_plain_bytes = UNSTREAM_STRING_ASCII( &constant_bin[ 55475 ], 5, 1 );
    const_str_plain_close = UNSTREAM_STRING_ASCII( &constant_bin[ 55480 ], 5, 1 );
    const_str_plain_dtype = UNSTREAM_STRING_ASCII( &constant_bin[ 50441 ], 5, 1 );
    const_str_plain_empty = UNSTREAM_STRING_ASCII( &constant_bin[ 29873 ], 5, 1 );
    const_str_plain_heads = UNSTREAM_STRING_ASCII( &constant_bin[ 489 ], 5, 1 );
    const_str_plain_image = UNSTREAM_STRING_ASCII( &constant_bin[ 167 ], 5, 1 );
    const_str_plain_int32 = UNSTREAM_STRING_ASCII( &constant_bin[ 41114 ], 5, 1 );
    const_str_plain_level = UNSTREAM_STRING_ASCII( &constant_bin[ 21295 ], 5, 1 );
    const_str_plain_lower = UNSTREAM_STRING_ASCII( &constant_bin[ 55485 ], 5, 1 );
    const_str_plain_masks = UNSTREAM_STRING_ASCII( &constant_bin[ 592 ], 5, 1 );
    const_str_plain_model = UNSTREAM_STRING_ASCII( &constant_bin[ 2143 ], 5, 1 );
    const_str_plain_names = UNSTREAM_STRING_ASCII( &constant_bin[ 6354 ], 5, 1 );
    const_str_plain_numpy = UNSTREAM_STRING_ASCII( &constant_bin[ 3568 ], 5, 1 );
    const_str_plain_print = UNSTREAM_STRING_ASCII( &constant_bin[ 13392 ], 5, 1 );
    const_str_plain_range = UNSTREAM_STRING_ASCII( &constant_bin[ 271 ], 5, 1 );
    const_str_plain_round = UNSTREAM_STRING_ASCII( &constant_bin[ 6222 ], 5, 1 );
    const_str_plain_scale = UNSTREAM_STRING_ASCII( &constant_bin[ 9081 ], 5, 1 );
    const_str_plain_shape = UNSTREAM_STRING_ASCII( &constant_bin[ 862 ], 5, 1 );
    const_str_plain_shift = UNSTREAM_STRING_ASCII( &constant_bin[ 22181 ], 5, 1 );
    const_str_plain_split = UNSTREAM_STRING_ASCII( &constant_bin[ 55490 ], 5, 1 );
    const_str_plain_stack = UNSTREAM_STRING_ASCII( &constant_bin[ 36588 ], 5, 1 );
    const_str_plain_throw = UNSTREAM_STRING_ASCII( &constant_bin[ 55495 ], 5, 1 );
    const_str_plain_train = UNSTREAM_STRING_ASCII( &constant_bin[ 214 ], 5, 1 );
    const_str_plain_tuple = UNSTREAM_STRING_ASCII( &constant_bin[ 43599 ], 5, 1 );
    const_str_plain_types = UNSTREAM_STRING_ASCII( &constant_bin[ 55500 ], 5, 1 );
    const_str_plain_uint8 = UNSTREAM_STRING_ASCII( &constant_bin[ 55505 ], 5, 1 );
    const_str_plain_where = UNSTREAM_STRING_ASCII( &constant_bin[ 9766 ], 5, 1 );
    const_str_plain_width = UNSTREAM_STRING_ASCII( &constant_bin[ 794 ], 5, 1 );
    const_str_plain_zeros = UNSTREAM_STRING_ASCII( &constant_bin[ 13518 ], 5, 1 );
    const_str_plain_Config = UNSTREAM_STRING_ASCII( &constant_bin[ 1783 ], 6, 1 );
    const_str_plain_Fliplr = UNSTREAM_STRING_ASCII( &constant_bin[ 23388 ], 6, 1 );
    const_str_plain_append = UNSTREAM_STRING_ASCII( &constant_bin[ 55510 ], 6, 1 );
    const_str_plain_arange = UNSTREAM_STRING_ASCII( &constant_bin[ 55516 ], 6, 1 );
    const_str_plain_argmax = UNSTREAM_STRING_ASCII( &constant_bin[ 18419 ], 6, 1 );
    const_str_plain_around = UNSTREAM_STRING_ASCII( &constant_bin[ 55522 ], 6, 1 );
    const_str_plain_astype = UNSTREAM_STRING_ASCII( &constant_bin[ 55528 ], 6, 1 );
    const_str_plain_config = UNSTREAM_STRING_ASCII( &constant_bin[ 392 ], 6, 1 );
    const_str_plain_counts = UNSTREAM_STRING_ASCII( &constant_bin[ 17515 ], 6, 1 );
    const_str_plain_delete = UNSTREAM_STRING_ASCII( &constant_bin[ 55534 ], 6, 1 );
    const_str_plain_deltas = UNSTREAM_STRING_ASCII( &constant_bin[ 10424 ], 6, 1 );
    const_str_plain_detect = UNSTREAM_STRING_ASCII( &constant_bin[ 7311 ], 6, 1 );
    const_str_plain_divide = UNSTREAM_STRING_ASCII( &constant_bin[ 49325 ], 6, 1 );
    const_str_plain_epochs = UNSTREAM_STRING_ASCII( &constant_bin[ 22580 ], 6, 1 );
    const_str_plain_exists = UNSTREAM_STRING_ASCII( &constant_bin[ 55540 ], 6, 1 );
    const_str_plain_extend = UNSTREAM_STRING_ASCII( &constant_bin[ 55546 ], 6, 1 );
    const_str_plain_format = UNSTREAM_STRING_ASCII( &constant_bin[ 332 ], 6, 1 );
    const_str_plain_height = UNSTREAM_STRING_ASCII( &constant_bin[ 786 ], 6, 1 );
    const_str_plain_images = UNSTREAM_STRING_ASCII( &constant_bin[ 167 ], 6, 1 );
    const_str_plain_imgaug = UNSTREAM_STRING_ASCII( &constant_bin[ 9103 ], 6, 1 );
    const_str_plain_inputs = UNSTREAM_STRING_ASCII( &constant_bin[ 8271 ], 6, 1 );
    const_str_plain_kwargs = UNSTREAM_STRING_ASCII( &constant_bin[ 55552 ], 6, 1 );
    const_str_plain_layers = UNSTREAM_STRING_ASCII( &constant_bin[ 4974 ], 6, 1 );
    const_str_plain_locals = UNSTREAM_STRING_ASCII( &constant_bin[ 14245 ], 6, 1 );
    const_str_plain_object = UNSTREAM_STRING_ASCII( &constant_bin[ 1528 ], 6, 1 );
    const_str_plain_origin = UNSTREAM_STRING_ASCII( &constant_bin[ 7421 ], 6, 1 );
    const_str_plain_random = UNSTREAM_STRING_ASCII( &constant_bin[ 11767 ], 6, 1 );
    const_str_plain_resize = UNSTREAM_STRING_ASCII( &constant_bin[ 11242 ], 6, 1 );
    const_str_plain_result = UNSTREAM_STRING_ASCII( &constant_bin[ 1717 ], 6, 1 );
    const_str_plain_scores = UNSTREAM_STRING_ASCII( &constant_bin[ 7368 ], 6, 1 );
    const_str_plain_shutil = UNSTREAM_STRING_ASCII( &constant_bin[ 55558 ], 6, 1 );
    const_str_plain_sorted = UNSTREAM_STRING_ASCII( &constant_bin[ 49429 ], 6, 1 );
    const_str_plain_source = UNSTREAM_STRING_ASCII( &constant_bin[ 9194 ], 6, 1 );
    const_str_plain_square = UNSTREAM_STRING_ASCII( &constant_bin[ 24766 ], 6, 1 );
    const_str_plain_urllib = UNSTREAM_STRING_ASCII( &constant_bin[ 55564 ], 6, 1 );
    const_tuple_none_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_none_tuple, 0, Py_None ); Py_INCREF( Py_None );
    const_str_plain_Dataset = UNSTREAM_STRING_ASCII( &constant_bin[ 498 ], 7, 1 );
    const_str_plain___all__ = UNSTREAM_STRING_ASCII( &constant_bin[ 55570 ], 7, 1 );
    const_str_plain___cmp__ = UNSTREAM_STRING_ASCII( &constant_bin[ 55577 ], 7, 1 );
    const_str_plain___doc__ = UNSTREAM_STRING_ASCII( &constant_bin[ 55584 ], 7, 1 );
    const_str_plain___model = UNSTREAM_STRING_ASCII( &constant_bin[ 33092 ], 7, 1 );
    const_str_plain___utils = UNSTREAM_STRING_ASCII( &constant_bin[ 43947 ], 7, 1 );
    const_str_plain_abspath = UNSTREAM_STRING_ASCII( &constant_bin[ 55591 ], 7, 1 );
    const_str_plain_anchors = UNSTREAM_STRING_ASCII( &constant_bin[ 8869 ], 7, 1 );
    const_str_plain_by_name = UNSTREAM_STRING_ASCII( &constant_bin[ 12659 ], 7, 1 );
    const_str_plain_compile = UNSTREAM_STRING_ASCII( &constant_bin[ 20337 ], 7, 1 );
    const_str_plain_default = UNSTREAM_STRING_ASCII( &constant_bin[ 2879 ], 7, 1 );
    const_str_plain_display = UNSTREAM_STRING_ASCII( &constant_bin[ 6035 ], 7, 1 );
    const_str_plain_float32 = UNSTREAM_STRING_ASCII( &constant_bin[ 38160 ], 7, 1 );
    const_str_plain_globals = UNSTREAM_STRING_ASCII( &constant_bin[ 55598 ], 7, 1 );
    const_str_plain_indices = UNSTREAM_STRING_ASCII( &constant_bin[ 21355 ], 7, 1 );
    const_str_plain_inspect = UNSTREAM_STRING_ASCII( &constant_bin[ 8341 ], 7, 1 );
    const_str_plain_logging = UNSTREAM_STRING_ASCII( &constant_bin[ 55605 ], 7, 1 );
    const_str_plain_maximum = UNSTREAM_STRING_ASCII( &constant_bin[ 48668 ], 7, 1 );
    const_str_plain_minimum = UNSTREAM_STRING_ASCII( &constant_bin[ 55612 ], 7, 1 );
    const_str_plain_outputs = UNSTREAM_STRING_ASCII( &constant_bin[ 12261 ], 7, 1 );
    const_str_plain_padding = UNSTREAM_STRING_ASCII( &constant_bin[ 9088 ], 7, 1 );
    const_str_plain_prepare = UNSTREAM_STRING_ASCII( &constant_bin[ 51083 ], 7, 1 );
    const_str_plain_randint = UNSTREAM_STRING_ASCII( &constant_bin[ 55619 ], 7, 1 );
    const_str_plain_request = UNSTREAM_STRING_ASCII( &constant_bin[ 1076 ], 7, 1 );
    const_str_plain_reshape = UNSTREAM_STRING_ASCII( &constant_bin[ 55626 ], 7, 1 );
    const_str_plain_results = UNSTREAM_STRING_ASCII( &constant_bin[ 1717 ], 7, 1 );
    const_str_plain_urlopen = UNSTREAM_STRING_ASCII( &constant_bin[ 55633 ], 7, 1 );
    const_str_plain_verbose = UNSTREAM_STRING_ASCII( &constant_bin[ 55640 ], 7, 1 );
    const_str_plain_warning = UNSTREAM_STRING_ASCII( &constant_bin[ 49421 ], 7, 1 );
    const_str_angle_listcomp = UNSTREAM_STRING_ASCII( &constant_bin[ 55647 ], 10, 0 );
    const_str_plain_BACKBONE = UNSTREAM_STRING_ASCII( &constant_bin[ 55657 ], 8, 1 );
    const_str_plain_Ellipsis = UNSTREAM_STRING_ASCII( &constant_bin[ 55665 ], 8, 1 );
    const_str_plain_MaskRCNN = UNSTREAM_STRING_ASCII( &constant_bin[ 7213 ], 8, 1 );
    const_str_plain_ROOT_DIR = UNSTREAM_STRING_ASCII( &constant_bin[ 55673 ], 8, 1 );
    const_str_plain_TRAIN_BN = UNSTREAM_STRING_ASCII( &constant_bin[ 55681 ], 8, 1 );
    const_str_plain___dict__ = UNSTREAM_STRING_ASCII( &constant_bin[ 55689 ], 8, 1 );
    const_str_plain___exit__ = UNSTREAM_STRING_ASCII( &constant_bin[ 55697 ], 8, 1 );
    const_str_plain___file__ = UNSTREAM_STRING_ASCII( &constant_bin[ 55705 ], 8, 1 );
    const_str_plain___init__ = UNSTREAM_STRING_ASCII( &constant_bin[ 54 ], 8, 1 );
    const_str_plain___iter__ = UNSTREAM_STRING_ASCII( &constant_bin[ 55713 ], 8, 1 );
    const_str_plain___name__ = UNSTREAM_STRING_ASCII( &constant_bin[ 55721 ], 8, 1 );
    const_str_plain___path__ = UNSTREAM_STRING_ASCII( &constant_bin[ 55729 ], 8, 1 );
    const_str_plain___spec__ = UNSTREAM_STRING_ASCII( &constant_bin[ 55737 ], 8, 1 );
    const_str_plain_callable = UNSTREAM_STRING_ASCII( &constant_bin[ 55745 ], 8, 1 );
    const_str_plain_center_x = UNSTREAM_STRING_ASCII( &constant_bin[ 31149 ], 8, 1 );
    const_str_plain_center_y = UNSTREAM_STRING_ASCII( &constant_bin[ 31136 ], 8, 1 );
    const_str_plain_class_id = UNSTREAM_STRING_ASCII( &constant_bin[ 948 ], 8, 1 );
    const_str_plain_constant = UNSTREAM_STRING_ASCII( &constant_bin[ 55753 ], 8, 1 );
    const_str_plain_fromlist = UNSTREAM_STRING_ASCII( &constant_bin[ 55761 ], 8, 1 );
    const_str_plain_gt_boxes = UNSTREAM_STRING_ASCII( &constant_bin[ 14837 ], 8, 1 );
    const_str_plain_gt_masks = UNSTREAM_STRING_ASCII( &constant_bin[ 14886 ], 8, 1 );
    const_str_plain_image_id = UNSTREAM_STRING_ASCII( &constant_bin[ 348 ], 8, 1 );
    const_str_plain_makedirs = UNSTREAM_STRING_ASCII( &constant_bin[ 55769 ], 8, 1 );
    const_str_plain_multiply = UNSTREAM_STRING_ASCII( &constant_bin[ 55777 ], 8, 1 );
    const_str_plain_terminal = UNSTREAM_STRING_ASCII( &constant_bin[ 55785 ], 8, 1 );
    const_str_plain_training = UNSTREAM_STRING_ASCII( &constant_bin[ 2441 ], 8, 1 );
    const_str_angle_metaclass = UNSTREAM_STRING_ASCII( &constant_bin[ 55793 ], 11, 0 );
    const_str_plain_GPU_COUNT = UNSTREAM_STRING_ASCII( &constant_bin[ 55804 ], 9, 1 );
    const_str_plain_POOL_SIZE = UNSTREAM_STRING_ASCII( &constant_bin[ 24991 ], 9, 1 );
    const_str_plain___class__ = UNSTREAM_STRING_ASCII( &constant_bin[ 55813 ], 9, 1 );
    const_str_plain___debug__ = UNSTREAM_STRING_ASCII( &constant_bin[ 55822 ], 9, 1 );
    const_str_plain___enter__ = UNSTREAM_STRING_ASCII( &constant_bin[ 55831 ], 9, 1 );
    const_str_plain_add_class = UNSTREAM_STRING_ASCII( &constant_bin[ 52989 ], 9, 1 );
    const_str_plain_add_image = UNSTREAM_STRING_ASCII( &constant_bin[ 52053 ], 9, 1 );
    const_str_plain_bytearray = UNSTREAM_STRING_ASCII( &constant_bin[ 55840 ], 9, 1 );
    const_str_plain_class_ids = UNSTREAM_STRING_ASCII( &constant_bin[ 948 ], 9, 1 );
    const_str_plain_class_map = UNSTREAM_STRING_ASCII( &constant_bin[ 4429 ], 9, 1 );
    const_str_plain_enumerate = UNSTREAM_STRING_ASCII( &constant_bin[ 55849 ], 9, 1 );
    const_str_plain_find_last = UNSTREAM_STRING_ASCII( &constant_bin[ 21819 ], 9, 1 );
    const_str_plain_image_ids = UNSTREAM_STRING_ASCII( &constant_bin[ 348 ], 9, 1 );
    const_str_plain_inference = UNSTREAM_STRING_ASCII( &constant_bin[ 14055 ], 9, 1 );
    const_str_plain_load_mask = UNSTREAM_STRING_ASCII( &constant_bin[ 5587 ], 9, 1 );
    const_str_plain_metaclass = UNSTREAM_STRING_ASCII( &constant_bin[ 55794 ], 9, 1 );
    const_str_plain_model_dir = UNSTREAM_STRING_ASCII( &constant_bin[ 42104 ], 9, 1 );
    const_str_plain_resnet101 = UNSTREAM_STRING_ASCII( &constant_bin[ 26397 ], 9, 1 );
    const_slice_none_none_none = PySlice_New( Py_None, Py_None, Py_None );
    const_str_plain_BATCH_SIZE = UNSTREAM_STRING_ASCII( &constant_bin[ 17119 ], 10, 1 );
    const_str_plain_CocoConfig = UNSTREAM_STRING_ASCII( &constant_bin[ 6405 ], 10, 1 );
    const_str_plain_MASK_SHAPE = UNSTREAM_STRING_ASCII( &constant_bin[ 29834 ], 10, 1 );
    const_str_plain_MEAN_PIXEL = UNSTREAM_STRING_ASCII( &constant_bin[ 55858 ], 10, 1 );
    const_str_plain___cached__ = UNSTREAM_STRING_ASCII( &constant_bin[ 55868 ], 10, 1 );
    const_str_plain___import__ = UNSTREAM_STRING_ASCII( &constant_bin[ 55878 ], 10, 1 );
    const_str_plain___loader__ = UNSTREAM_STRING_ASCII( &constant_bin[ 55888 ], 10, 1 );
    const_str_plain___module__ = UNSTREAM_STRING_ASCII( &constant_bin[ 55898 ], 10, 1 );
    const_str_plain_batch_size = UNSTREAM_STRING_ASCII( &constant_bin[ 19841 ], 10, 1 );
    const_str_plain_image_info = UNSTREAM_STRING_ASCII( &constant_bin[ 55908 ], 10, 1 );
    const_str_plain_load_image = UNSTREAM_STRING_ASCII( &constant_bin[ 8423 ], 10, 1 );
    const_str_plain_model_path = UNSTREAM_STRING_ASCII( &constant_bin[ 38479 ], 10, 1 );
    const_str_plain_norm_boxes = UNSTREAM_STRING_ASCII( &constant_bin[ 26318 ], 10, 1 );
    const_str_plain_pred_masks = UNSTREAM_STRING_ASCII( &constant_bin[ 38303 ], 10, 1 );
    const_str_plain_startswith = UNSTREAM_STRING_ASCII( &constant_bin[ 55918 ], 10, 1 );
    const_str_plain_tensorflow = UNSTREAM_STRING_ASCII( &constant_bin[ 55928 ], 10, 1 );
    const_str_plain_trim_zeros = UNSTREAM_STRING_ASCII( &constant_bin[ 43248 ], 10, 1 );
    const_str_plain_IMAGE_SHAPE = UNSTREAM_STRING_ASCII( &constant_bin[ 55938 ], 11, 1 );
    const_str_plain_NUM_CLASSES = UNSTREAM_STRING_ASCII( &constant_bin[ 15152 ], 11, 1 );
    const_str_plain___getitem__ = UNSTREAM_STRING_ASCII( &constant_bin[ 55949 ], 11, 1 );
    const_str_plain___package__ = UNSTREAM_STRING_ASCII( &constant_bin[ 55960 ], 11, 1 );
    const_str_plain___prepare__ = UNSTREAM_STRING_ASCII( &constant_bin[ 55971 ], 11, 1 );
    const_str_plain___version__ = UNSTREAM_STRING_ASCII( &constant_bin[ 55982 ], 11, 1 );
    const_str_plain_batch_slice = UNSTREAM_STRING_ASCII( &constant_bin[ 55993 ], 11, 1 );
    const_str_plain_classmethod = UNSTREAM_STRING_ASCII( &constant_bin[ 56004 ], 11, 1 );
    const_str_plain_compute_iou = UNSTREAM_STRING_ASCII( &constant_bin[ 56015 ], 11, 1 );
    const_str_plain_concatenate = UNSTREAM_STRING_ASCII( &constant_bin[ 56026 ], 11, 1 );
    const_str_plain_copyfileobj = UNSTREAM_STRING_ASCII( &constant_bin[ 56037 ], 11, 1 );
    const_str_plain_image_shape = UNSTREAM_STRING_ASCII( &constant_bin[ 7430 ], 11, 1 );
    const_str_plain_num_classes = UNSTREAM_STRING_ASCII( &constant_bin[ 9528 ], 11, 1 );
    const_str_plain_resize_mask = UNSTREAM_STRING_ASCII( &constant_bin[ 56048 ], 11, 1 );
    const_str_plain_unmold_mask = UNSTREAM_STRING_ASCII( &constant_bin[ 56059 ], 11, 1 );
    const_tuple_float_0_5_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_float_0_5_tuple, 0, const_float_0_5 ); Py_INCREF( const_float_0_5 );
    const_tuple_int_pos_1_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_int_pos_1_tuple, 0, const_int_pos_1 ); Py_INCREF( const_int_pos_1 );
    const_tuple_type_bool_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_type_bool_tuple, 0, (PyObject *)&PyBool_Type ); Py_INCREF( (PyObject *)&PyBool_Type );
    const_str_plain_BBOX_STD_DEV = UNSTREAM_STRING_ASCII( &constant_bin[ 56070 ], 12, 1 );
    const_str_plain_LOSS_WEIGHTS = UNSTREAM_STRING_ASCII( &constant_bin[ 56082 ], 12, 1 );
    const_str_plain_LooseVersion = UNSTREAM_STRING_ASCII( &constant_bin[ 56094 ], 12, 1 );
    const_str_plain_USE_RPN_ROIS = UNSTREAM_STRING_ASCII( &constant_bin[ 56106 ], 12, 1 );
    const_str_plain_WEIGHT_DECAY = UNSTREAM_STRING_ASCII( &constant_bin[ 56118 ], 12, 1 );
    const_str_plain___builtins__ = UNSTREAM_STRING_ASCII( &constant_bin[ 56130 ], 12, 1 );
    const_str_plain___compiled__ = UNSTREAM_STRING_ASCII( &constant_bin[ 56142 ], 12, 1 );
    const_str_plain___internal__ = UNSTREAM_STRING_ASCII( &constant_bin[ 56154 ], 12, 1 );
    const_str_plain___qualname__ = UNSTREAM_STRING_ASCII( &constant_bin[ 56166 ], 12, 1 );
    const_str_plain_augmentation = UNSTREAM_STRING_ASCII( &constant_bin[ 9004 ], 12, 1 );
    const_str_plain_denorm_boxes = UNSTREAM_STRING_ASCII( &constant_bin[ 43264 ], 12, 1 );
    const_str_plain_gt_class_ids = UNSTREAM_STRING_ASCII( &constant_bin[ 11708 ], 12, 1 );
    const_str_plain_has_location = UNSTREAM_STRING_ASCII( &constant_bin[ 56178 ], 12, 1 );
    const_str_plain_load_weights = UNSTREAM_STRING_ASCII( &constant_bin[ 12630 ], 12, 1 );
    const_str_plain_resize_image = UNSTREAM_STRING_ASCII( &constant_bin[ 44866 ], 12, 1 );
    const_str_plain_staticmethod = UNSTREAM_STRING_ASCII( &constant_bin[ 56190 ], 12, 1 );
    const_str_plain_IMAGE_MAX_DIM = UNSTREAM_STRING_ASCII( &constant_bin[ 56202 ], 13, 1 );
    const_str_plain_IMAGE_MIN_DIM = UNSTREAM_STRING_ASCII( &constant_bin[ 56215 ], 13, 1 );
    const_str_plain_LEARNING_RATE = UNSTREAM_STRING_ASCII( &constant_bin[ 56228 ], 13, 1 );
    const_str_plain_PRE_NMS_LIMIT = UNSTREAM_STRING_ASCII( &constant_bin[ 56241 ], 13, 1 );
    const_str_plain_USE_MINI_MASK = UNSTREAM_STRING_ASCII( &constant_bin[ 56254 ], 13, 1 );
    const_str_plain___metaclass__ = UNSTREAM_STRING_ASCII( &constant_bin[ 56267 ], 13, 1 );
    const_str_plain__initializing = UNSTREAM_STRING_ASCII( &constant_bin[ 56280 ], 13, 1 );
    const_str_plain_anchor_stride = UNSTREAM_STRING_ASCII( &constant_bin[ 12019 ], 13, 1 );
    const_str_plain_iou_threshold = UNSTREAM_STRING_ASCII( &constant_bin[ 45718 ], 13, 1 );
    const_str_plain_learning_rate = UNSTREAM_STRING_ASCII( &constant_bin[ 22525 ], 13, 1 );
    const_str_plain_minimize_mask = UNSTREAM_STRING_ASCII( &constant_bin[ 51864 ], 13, 1 );
    const_str_plain_rpn_bbox_loss = UNSTREAM_STRING_ASCII( &constant_bin[ 10857 ], 13, 1 );
    const_tuple_int_0_int_0_tuple = PyTuple_New( 2 );
    PyTuple_SET_ITEM( const_tuple_int_0_int_0_tuple, 0, const_int_0 ); Py_INCREF( const_int_0 );
    PyTuple_SET_ITEM( const_tuple_int_0_int_0_tuple, 1, const_int_0 ); Py_INCREF( const_int_0 );
    const_tuple_str_plain_x_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_str_plain_x_tuple, 0, const_str_plain_x ); Py_INCREF( const_str_plain_x );
    const_tuple_type_object_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_type_object_tuple, 0, (PyObject *)&PyBaseObject_Type ); Py_INCREF( (PyObject *)&PyBaseObject_Type );
    const_str_plain_IMAGES_PER_GPU = UNSTREAM_STRING_ASCII( &constant_bin[ 56293 ], 14, 1 );
    const_str_plain_MASK_POOL_SIZE = UNSTREAM_STRING_ASCII( &constant_bin[ 24986 ], 14, 1 );
    const_str_plain_box_refinement = UNSTREAM_STRING_ASCII( &constant_bin[ 56307 ], 14, 1 );
    const_str_plain_extract_bboxes = UNSTREAM_STRING_ASCII( &constant_bin[ 56321 ], 14, 1 );
    const_str_plain_pred_class_ids = UNSTREAM_STRING_ASCII( &constant_bin[ 56335 ], 14, 1 );
    const_str_plain_rpn_class_loss = UNSTREAM_STRING_ASCII( &constant_bin[ 32472 ], 14, 1 );
    const_slice_int_pos_1_none_none = PySlice_New( const_int_pos_1, Py_None, Py_None );
    const_slice_none_int_pos_2_none = PySlice_New( Py_None, const_int_pos_2, Py_None );
    const_slice_none_int_pos_4_none = PySlice_New( Py_None, const_int_pos_4, Py_None );
    const_slice_none_none_int_neg_1 = PySlice_New( Py_None, Py_None, const_int_neg_1 );
    const_str_plain_COCO_MODEL_PATH = UNSTREAM_STRING_ASCII( &constant_bin[ 56349 ], 15, 1 );
    const_str_plain_IMAGE_META_SIZE = UNSTREAM_STRING_ASCII( &constant_bin[ 56364 ], 15, 1 );
    const_str_plain_IMAGE_MIN_SCALE = UNSTREAM_STRING_ASCII( &constant_bin[ 56379 ], 15, 1 );
    const_str_plain_MINI_MASK_SHAPE = UNSTREAM_STRING_ASCII( &constant_bin[ 29829 ], 15, 1 );
    const_str_plain_STEPS_PER_EPOCH = UNSTREAM_STRING_ASCII( &constant_bin[ 56394 ], 15, 1 );
    const_str_plain_constant_values = UNSTREAM_STRING_ASCII( &constant_bin[ 56409 ], 15, 1 );
    const_str_plain_image_reference = UNSTREAM_STRING_ASCII( &constant_bin[ 4722 ], 15, 1 );
    const_str_plain_mrcnn_bbox_loss = UNSTREAM_STRING_ASCII( &constant_bin[ 27680 ], 15, 1 );
    const_str_plain_mrcnn_mask_loss = UNSTREAM_STRING_ASCII( &constant_bin[ 17604 ], 15, 1 );
    const_str_plain_BACKBONE_STRIDES = UNSTREAM_STRING_ASCII( &constant_bin[ 56424 ], 16, 1 );
    const_str_plain_MAX_GT_INSTANCES = UNSTREAM_STRING_ASCII( &constant_bin[ 25527 ], 16, 1 );
    const_str_plain_RPN_BBOX_STD_DEV = UNSTREAM_STRING_ASCII( &constant_bin[ 56440 ], 16, 1 );
    const_str_plain_VALIDATION_STEPS = UNSTREAM_STRING_ASCII( &constant_bin[ 56456 ], 16, 1 );
    const_str_plain_compute_overlaps = UNSTREAM_STRING_ASCII( &constant_bin[ 53890 ], 16, 1 );
    const_str_plain_mrcnn_class_loss = UNSTREAM_STRING_ASCII( &constant_bin[ 20812 ], 16, 1 );
    const_str_plain_source_class_ids = UNSTREAM_STRING_ASCII( &constant_bin[ 9194 ], 16, 1 );
    const_tuple_none_none_none_tuple = PyTuple_New( 3 );
    PyTuple_SET_ITEM( const_tuple_none_none_none_tuple, 0, Py_None ); Py_INCREF( Py_None );
    PyTuple_SET_ITEM( const_tuple_none_none_none_tuple, 1, Py_None ); Py_INCREF( Py_None );
    PyTuple_SET_ITEM( const_tuple_none_none_none_tuple, 2, Py_None ); Py_INCREF( Py_None );
    const_tuple_str_plain_self_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_str_plain_self_tuple, 0, const_str_plain_self ); Py_INCREF( const_str_plain_self );
    const_str_plain_IMAGE_RESIZE_MODE = UNSTREAM_STRING_ASCII( &constant_bin[ 17235 ], 17, 1 );
    const_str_plain_LEARNING_MOMENTUM = UNSTREAM_STRING_ASCII( &constant_bin[ 56472 ], 17, 1 );
    const_str_plain_RPN_ANCHOR_RATIOS = UNSTREAM_STRING_ASCII( &constant_bin[ 56489 ], 17, 1 );
    const_str_plain_RPN_ANCHOR_SCALES = UNSTREAM_STRING_ASCII( &constant_bin[ 56506 ], 17, 1 );
    const_str_plain_RPN_ANCHOR_STRIDE = UNSTREAM_STRING_ASCII( &constant_bin[ 56523 ], 17, 1 );
    const_str_plain_RPN_NMS_THRESHOLD = UNSTREAM_STRING_ASCII( &constant_bin[ 56540 ], 17, 1 );
    const_str_plain_GRADIENT_CLIP_NORM = UNSTREAM_STRING_ASCII( &constant_bin[ 56557 ], 18, 1 );
    const_str_plain_ROI_POSITIVE_RATIO = UNSTREAM_STRING_ASCII( &constant_bin[ 56575 ], 18, 1 );
    const_str_plain_get_source_class_id = UNSTREAM_STRING_ASCII( &constant_bin[ 44071 ], 19, 1 );
    const_str_plain_map_source_class_id = UNSTREAM_STRING_ASCII( &constant_bin[ 44527 ], 19, 1 );
    const_str_plain_non_max_suppression = UNSTREAM_STRING_ASCII( &constant_bin[ 7225 ], 19, 1 );
    const_str_plain_TRAIN_ROIS_PER_IMAGE = UNSTREAM_STRING_ASCII( &constant_bin[ 15019 ], 20, 1 );
    const_str_plain_box_refinement_graph = UNSTREAM_STRING_ASCII( &constant_bin[ 56593 ], 20, 1 );
    const_str_plain_get_imagenet_weights = UNSTREAM_STRING_ASCII( &constant_bin[ 33458 ], 20, 1 );
    const_tuple_str_plain_MaskRCNN_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_str_plain_MaskRCNN_tuple, 0, const_str_plain_MaskRCNN ); Py_INCREF( const_str_plain_MaskRCNN );
    const_str_plain_TOP_DOWN_PYRAMID_SIZE = UNSTREAM_STRING_ASCII( &constant_bin[ 56613 ], 21, 1 );
    const_tuple_str_plain___class___tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_str_plain___class___tuple, 0, const_str_plain___class__ ); Py_INCREF( const_str_plain___class__ );
    const_str_plain_COMPUTE_BACKBONE_SHAPE = UNSTREAM_STRING_ASCII( &constant_bin[ 56634 ], 22, 1 );
    const_str_plain_POST_NMS_ROIS_TRAINING = UNSTREAM_STRING_ASCII( &constant_bin[ 25368 ], 22, 1 );
    const_str_plain_DETECTION_MAX_INSTANCES = UNSTREAM_STRING_ASCII( &constant_bin[ 56656 ], 23, 1 );
    const_str_plain_DETECTION_NMS_THRESHOLD = UNSTREAM_STRING_ASCII( &constant_bin[ 56679 ], 23, 1 );
    const_str_plain_POST_NMS_ROIS_INFERENCE = UNSTREAM_STRING_ASCII( &constant_bin[ 56702 ], 23, 1 );
    const_str_plain_DETECTION_MIN_CONFIDENCE = UNSTREAM_STRING_ASCII( &constant_bin[ 56725 ], 24, 1 );
    const_str_plain_download_trained_weights = UNSTREAM_STRING_ASCII( &constant_bin[ 6447 ], 24, 1 );
    const_str_plain_generate_pyramid_anchors = UNSTREAM_STRING_ASCII( &constant_bin[ 56749 ], 24, 1 );
    const_tuple_str_plain_LooseVersion_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_str_plain_LooseVersion_tuple, 0, const_str_plain_LooseVersion ); Py_INCREF( const_str_plain_LooseVersion );
    const_tuple_str_plain_o_str_plain_n_tuple = PyTuple_New( 2 );
    PyTuple_SET_ITEM( const_tuple_str_plain_o_str_plain_n_tuple, 0, const_str_plain_o ); Py_INCREF( const_str_plain_o );
    PyTuple_SET_ITEM( const_tuple_str_plain_o_str_plain_n_tuple, 1, const_str_plain_n ); Py_INCREF( const_str_plain_n );
    const_str_plain_FPN_CLASSIF_FC_LAYERS_SIZE = UNSTREAM_STRING_ASCII( &constant_bin[ 56773 ], 26, 1 );
    const_str_plain_submodule_search_locations = UNSTREAM_STRING_ASCII( &constant_bin[ 56799 ], 26, 1 );
    const_dict_54f4aa72cf3f950a22814f798a2888e8 = _PyDict_NewPresized( 1 );
    PyDict_SetItem( const_dict_54f4aa72cf3f950a22814f798a2888e8, const_str_plain_axis, const_int_0 );
    assert( PyDict_Size( const_dict_54f4aa72cf3f950a22814f798a2888e8 ) == 1 );
    const_dict_72c7b31d39de2eb4cb1f11a06c118ebc = _PyDict_NewPresized( 1 );
    PyDict_SetItem( const_dict_72c7b31d39de2eb4cb1f11a06c118ebc, const_str_plain_verbose, const_int_0 );
    assert( PyDict_Size( const_dict_72c7b31d39de2eb4cb1f11a06c118ebc ) == 1 );
    const_dict_8a6ce79bb59f45c062c2a0027a3a0c33 = _PyDict_NewPresized( 1 );
    PyDict_SetItem( const_dict_8a6ce79bb59f45c062c2a0027a3a0c33, const_str_plain_dtype, (PyObject *)&PyBool_Type );
    assert( PyDict_Size( const_dict_8a6ce79bb59f45c062c2a0027a3a0c33 ) == 1 );
    const_dict_9e8fa581e6a44c6d65a10c615ae35aa0 = _PyDict_NewPresized( 1 );
    PyDict_SetItem( const_dict_9e8fa581e6a44c6d65a10c615ae35aa0, const_str_plain_by_name, Py_True );
    assert( PyDict_Size( const_dict_9e8fa581e6a44c6d65a10c615ae35aa0 ) == 1 );
    const_dict_a706c749f33afbbf180a37810efcd0ba = _PyDict_NewPresized( 1 );
    PyDict_SetItem( const_dict_a706c749f33afbbf180a37810efcd0ba, const_str_plain_axis, const_int_pos_2 );
    assert( PyDict_Size( const_dict_a706c749f33afbbf180a37810efcd0ba ) == 1 );
    const_dict_c4b01644824ba6bad132707fcdaa03f1 = _PyDict_NewPresized( 1 );
    PyDict_SetItem( const_dict_c4b01644824ba6bad132707fcdaa03f1, const_str_plain_axis, const_int_pos_1 );
    assert( PyDict_Size( const_dict_c4b01644824ba6bad132707fcdaa03f1 ) == 1 );
    const_str_plain_RPN_TRAIN_ANCHORS_PER_IMAGE = UNSTREAM_STRING_ASCII( &constant_bin[ 56825 ], 27, 1 );
    const_tuple_slice_none_none_none_int_0_tuple = PyTuple_New( 2 );
    PyTuple_SET_ITEM( const_tuple_slice_none_none_none_int_0_tuple, 0, const_slice_none_none_none ); Py_INCREF( const_slice_none_none_none );
    PyTuple_SET_ITEM( const_tuple_slice_none_none_none_int_0_tuple, 1, const_int_0 ); Py_INCREF( const_int_0 );
    const_list_int_0_int_0_int_pos_1_int_pos_1_list = PyList_New( 4 );
    PyList_SET_ITEM( const_list_int_0_int_0_int_pos_1_int_pos_1_list, 0, const_int_0 ); Py_INCREF( const_int_0 );
    PyList_SET_ITEM( const_list_int_0_int_0_int_pos_1_int_pos_1_list, 1, const_int_0 ); Py_INCREF( const_int_0 );
    PyList_SET_ITEM( const_list_int_0_int_0_int_pos_1_int_pos_1_list, 2, const_int_pos_1 ); Py_INCREF( const_int_pos_1 );
    PyList_SET_ITEM( const_list_int_0_int_0_int_pos_1_int_pos_1_list, 3, const_int_pos_1 ); Py_INCREF( const_int_pos_1 );
    const_tuple_slice_none_none_none_int_pos_1_tuple = PyTuple_New( 2 );
    PyTuple_SET_ITEM( const_tuple_slice_none_none_none_int_pos_1_tuple, 0, const_slice_none_none_none ); Py_INCREF( const_slice_none_none_none );
    PyTuple_SET_ITEM( const_tuple_slice_none_none_none_int_pos_1_tuple, 1, const_int_pos_1 ); Py_INCREF( const_int_pos_1 );
    const_tuple_slice_none_none_none_int_pos_2_tuple = PyTuple_New( 2 );
    PyTuple_SET_ITEM( const_tuple_slice_none_none_none_int_pos_2_tuple, 0, const_slice_none_none_none ); Py_INCREF( const_slice_none_none_none );
    PyTuple_SET_ITEM( const_tuple_slice_none_none_none_int_pos_2_tuple, 1, const_int_pos_2 ); Py_INCREF( const_int_pos_2 );
    const_tuple_slice_none_none_none_int_pos_3_tuple = PyTuple_New( 2 );
    PyTuple_SET_ITEM( const_tuple_slice_none_none_none_int_pos_3_tuple, 0, const_slice_none_none_none ); Py_INCREF( const_slice_none_none_none );
    PyTuple_SET_ITEM( const_tuple_slice_none_none_none_int_pos_3_tuple, 1, const_int_pos_3 ); Py_INCREF( const_int_pos_3 );
    const_str_digest_067240ca281436a921966038f28af45c = UNSTREAM_STRING_ASCII( &constant_bin[ 23169 ], 2, 0 );
    const_str_digest_22e74f88adcfbcd2c9bec40d576e19a9 = UNSTREAM_STRING_ASCII( &constant_bin[ 33352 ], 4, 0 );
    const_str_digest_25731c733fd74e8333aa29126ce85686 = UNSTREAM_STRING_ASCII( &constant_bin[ 8436 ], 2, 0 );
    const_str_digest_45e4dde2057b0bf276d6a84f4c917d27 = UNSTREAM_STRING_ASCII( &constant_bin[ 1527 ], 7, 0 );
    const_str_digest_4a0edff902aeaeff9fce1ee73187e8e1 = UNSTREAM_STRING_ASCII( &constant_bin[ 44034 ], 17, 0 );
    const_str_digest_4af59da437d2f21ccb08423e5fb98074 = UNSTREAM_STRING_ASCII( &constant_bin[ 56852 ], 17, 0 );
    const_str_digest_59bc9c95777e64e4720c3af0837aec42 = UNSTREAM_STRING_ASCII( &constant_bin[ 56869 ], 14, 0 );
    const_str_digest_75fd71b1edada749c2ef7ac810062295 = UNSTREAM_STRING_ASCII( &constant_bin[ 56883 ], 46, 0 );
    const_str_digest_9816e8d1552296af90d250823c964059 = UNSTREAM_STRING_ASCII( &constant_bin[ 56929 ], 46, 0 );
    const_str_digest_adc474dd61fbd736d69c1bac5d9712e0 = UNSTREAM_STRING_ASCII( &constant_bin[ 56975 ], 47, 0 );
    const_tuple_b709b748889c3a3b2974dc8135f76387_tuple = PyTuple_New( 6 );
    PyTuple_SET_ITEM( const_tuple_b709b748889c3a3b2974dc8135f76387_tuple, 0, const_str_plain_boxes ); Py_INCREF( const_str_plain_boxes );
    PyTuple_SET_ITEM( const_tuple_b709b748889c3a3b2974dc8135f76387_tuple, 1, const_str_plain_shape ); Py_INCREF( const_str_plain_shape );
    PyTuple_SET_ITEM( const_tuple_b709b748889c3a3b2974dc8135f76387_tuple, 2, const_str_plain_h ); Py_INCREF( const_str_plain_h );
    PyTuple_SET_ITEM( const_tuple_b709b748889c3a3b2974dc8135f76387_tuple, 3, const_str_plain_w ); Py_INCREF( const_str_plain_w );
    PyTuple_SET_ITEM( const_tuple_b709b748889c3a3b2974dc8135f76387_tuple, 4, const_str_plain_scale ); Py_INCREF( const_str_plain_scale );
    PyTuple_SET_ITEM( const_tuple_b709b748889c3a3b2974dc8135f76387_tuple, 5, const_str_plain_shift ); Py_INCREF( const_str_plain_shift );
    const_str_plain_get_human_and_background_from_a_frame = UNSTREAM_STRING_ASCII( &constant_bin[ 57022 ], 37, 1 );
    const_tuple_anon_function_anon_builtin_function_or_method_tuple = PyTuple_New( 2 );
    PyTuple_SET_ITEM( const_tuple_anon_function_anon_builtin_function_or_method_tuple, 0, (PyObject *)&PyFunction_Type ); Py_INCREF( (PyObject *)&PyFunction_Type );
    PyTuple_SET_ITEM( const_tuple_anon_function_anon_builtin_function_or_method_tuple, 1, (PyObject *)&PyCFunction_Type ); Py_INCREF( (PyObject *)&PyCFunction_Type );

#if _NUITKA_EXE
    /* Set the "sys.executable" path to the original CPython executable. */
    PySys_SetObject(
        (char *)"executable",
        None
    );

#ifndef _NUITKA_STANDALONE
    /* Set the "sys.prefix" path to the original one. */
    PySys_SetObject(
        (char *)"prefix",
        None
    );

    /* Set the "sys.prefix" path to the original one. */
    PySys_SetObject(
        (char *)"exec_prefix",
        None
    );


#if PYTHON_VERSION >= 300
    /* Set the "sys.base_prefix" path to the original one. */
    PySys_SetObject(
        (char *)"base_prefix",
        None
    );

    /* Set the "sys.exec_base_prefix" path to the original one. */
    PySys_SetObject(
        (char *)"base_exec_prefix",
        None
    );

#endif
#endif
#endif

    static PyTypeObject Nuitka_VersionInfoType;

    // Same fields as "sys.version_info" except no serial number.
    static PyStructSequence_Field Nuitka_VersionInfoFields[] = {
        {(char *)"major", (char *)"Major release number"},
        {(char *)"minor", (char *)"Minor release number"},
        {(char *)"micro", (char *)"Micro release number"},
        {(char *)"releaselevel", (char *)"'alpha', 'beta', 'candidate', or 'release'"},
        {0}
    };

    static PyStructSequence_Desc Nuitka_VersionInfoDesc = {
        (char *)"__nuitka_version__",                                    /* name */
        (char *)"__compiled__\n\nVersion information as a named tuple.", /* doc */
        Nuitka_VersionInfoFields,                                        /* fields */
        4
    };

    PyStructSequence_InitType(&Nuitka_VersionInfoType, &Nuitka_VersionInfoDesc);

    Nuitka_dunder_compiled_value = PyStructSequence_New(&Nuitka_VersionInfoType);
    assert(Nuitka_dunder_compiled_value != NULL);

    PyStructSequence_SET_ITEM(Nuitka_dunder_compiled_value, 0, PyInt_FromLong(0));
    PyStructSequence_SET_ITEM(Nuitka_dunder_compiled_value, 1, PyInt_FromLong(6));
    PyStructSequence_SET_ITEM(Nuitka_dunder_compiled_value, 2, PyInt_FromLong(3));

#if PYTHON_VERSION < 300
    PyStructSequence_SET_ITEM(Nuitka_dunder_compiled_value, 3, PyString_FromString("release"));
#else
    PyStructSequence_SET_ITEM(Nuitka_dunder_compiled_value, 3, PyUnicode_FromString("release"));
#endif
    // Prevent users from creating the Nuitka version type object.
    Nuitka_VersionInfoType.tp_init = NULL;
    Nuitka_VersionInfoType.tp_new = NULL;


}

// In debug mode we can check that the constants were not tampered with in any
// given moment. We typically do it at program exit, but we can add extra calls
// for sanity.
#ifndef __NUITKA_NO_ASSERT__
void checkGlobalConstants( void )
{

}
#endif

void createGlobalConstants( void )
{
    if ( _sentinel_value == NULL )
    {
#if PYTHON_VERSION < 300
        _sentinel_value = PyCObject_FromVoidPtr( NULL, NULL );
#else
        // The NULL value is not allowed for a capsule, so use something else.
        _sentinel_value = PyCapsule_New( (void *)27, "sentinel", NULL );
#endif
        assert( _sentinel_value );

        _createGlobalConstants();
    }
}
