# -*- coding: utf-8 -*-
"""
Created on Sat Aug 20 13:33:33 2016

***REMOVED***
"""
from sys import path

import numpy as np
import numpy.testing as npt

path.append("../..")
import lib_lkb.geometric_func as geo


# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
class test_ll_geo2ecef():
    #    def setUp(self):
    #        self.widget = Widget('The widget')

    #    #------------------------------------------------------------------
    #    def test_consistency_checks():
    #        #TODO
    #        pass
    #    #------------------------------------------------------------------


    # ------------------------------------------------------------------
    def test_specific_cases(self):
        # test of the function on some specific cases of lon and lat

        values_to_test = np.array([[0.0, 0], \
                                   [90.0, 0], \
                                   [0, 90.0], \
                                   [45, 0.0]]).T

        obtained_result = geo.ll_geoc2ecef(values_to_test)

        # expected values (derived from http://www.oc.nps.edu/oc2902w/coord/llhxyz.htm)         
        expected_result = np.array([[6378.1370, 0, 0], \
                                    [0, 6378.1370, 0], \
                                    [0, 0, 6378.1370],
                                    [4510.024, 4510.024, 0]]).T

        # test  
        npt.assert_allclose(obtained_result, expected_result, atol=1e-03, rtol=0)
        #        self.assertTrue(True)
        # ------------------------------------------------------------------

        #    #------------------------------------------------------------------
        #    def test_specific_cases():
        #         typically at lon = 180, etc.
        #        #TODO
        #        pass
        #    #------------------------------------------------------------------


# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>


# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
class test_compute_ecef_2_sc_rot_matrix():
    def test_function_consistency(self):
        # Outputs type depending on intput type shall be :
        # IN :             
        # nadir :              (3)INT or Float  | [3,X]  Int  or float
        # sat_pos :            (3)INT or Float  | [3,X]  Int  or float
        # normal_vector :      (3)INT or Float  | [3,X]  Int or float
        # _______________________________________|___________________________
        # OUT :                                 |             
        # matrix  :           [3,3]Fl           | [3,3, X]Fl
        #
        # If vectors do not have same dimension, the function shall error (?)


        # test with 1 dimension (INT only ; float would work too)
        nadir = np.array([6300, 0, 0])
        sat_pos = np.array([10000, 0, 0])
        normal_vector = np.array([0, 1, 0])

        result = geo.compute_ecef_2_sc_rot_matrix(nadir, sat_pos, normal_vector)

        npt.assert_equal(result.dtype == np.dtype('float64') and np.ndim(result) == 2, True)

        # test with 2 dimension vectors (INT only, float would work too)
        nadir = np.array([[6300, 0, 0]]).T
        sat_pos = np.array([[10000, 0, 0]]).T
        normal_vector = np.array([[0, 1, 0]]).T

        result = geo.compute_ecef_2_sc_rot_matrix(nadir, sat_pos, normal_vector)

        npt.assert_equal(result.dtype == np.dtype('float64') and np.ndim(result) == 3, True)

        # test with a mix of (3) and (3,1) vectors
        # TODO : this test fails ! where shall be addressed ?
        nadir = np.array([[6300, 0, 0]]).T
        sat_pos = np.array([10000, 0, 0])
        normal_vector = np.array([0, 1, 0])

        result = geo.compute_ecef_2_sc_rot_matrix(nadir, sat_pos, normal_vector)

        npt.assert_equal(result.dtype == np.dtype('float64') and np.ndim(result) == 3, True)


# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>


# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
class test_compute_xyz_rot_matrices():
    # TODO : tests of np.einsum function in all possible cases of vectors (1D, 2D, etc.)


    # ------------------------------------------------------------------------
    def test_consistency_xyz_rot_matrices(self):
        # Outputs type depending on intput type shall be :
        # IN :             
        # angle_x :    INT  | Float  | [X] of Int  | [X] of float
        # angle_y :    INT  | Float  | [X] of Int  | [X] of float
        # angle_z :    INT  | Float  | [X] of Int  | [X] of float
        # ___________________|________|_____________|_____________
        # OUT :             |        |             |
        # matrix  : [3,3]Fl | [3,3]Fl | [3,3, X]Fl | [3,3, X]Fl

        # Note : as everything goes through trigo functions (sine, cosine), int versus float problems
        # are already treated and therefore not tested here

        # test with scalars ############
        angle_x = 90.0 * np.pi / 180
        angle_y = 90.0 * np.pi / 180
        angle_z = 90.0 * np.pi / 180
        mat_rot = geo.compute_xyz_rot_matrices(angle_x, angle_y, angle_z)

        npt.assert_equal(np.ndim(mat_rot) == 2 and np.size(mat_rot) == 9, True)

        # test with (1) numpy arrays
        angle_x = np.array([90.0 * np.pi / 180])
        angle_y = np.array([90.0 * np.pi / 180])
        angle_z = np.array([90.0 * np.pi / 180])
        mat_rot = geo.compute_xyz_rot_matrices(angle_x, angle_y, angle_z)

        npt.assert_equal(np.ndim(mat_rot) == 3 and np.size(mat_rot) == 9, True)

        # test with (2) numpy arrays
        angle_x = np.array([90.0 * np.pi / 180, 90.0 * np.pi / 180])
        angle_y = np.array([90.0 * np.pi / 180, 90.0 * np.pi / 180])
        angle_z = np.array([90.0 * np.pi / 180, 90.0 * np.pi / 180])
        mat_rot = geo.compute_xyz_rot_matrices(angle_x, angle_y, angle_z)

        npt.assert_equal(np.ndim(mat_rot) == 3 and np.size(mat_rot) == 18, True)


        # TODO : one additional check can be to bring back bigger vectors into right size (for exampple [X,
        # 1] vectors into [X])

    # ------------------------------------------------------------------------
    def test_specific_values_xyz_rot_matrices(self):
        # test over some hand-computed examples

        # test 1 :        
        test_value = np.array([1, 0, 0.0])
        roll = 0.0
        pitch = 0.0
        yaw = 45.0 * np.pi / 180
        mat_rot = geo.compute_xyz_rot_matrices(roll, pitch, yaw)

        # todo : other specific tests

        obtained_result = np.dot(mat_rot, test_value)

        expected_result = np.array([1.0 / 2 ** 0.5, 1.0 / 2 ** 0.5, 0])

        npt.assert_allclose(obtained_result, expected_result, atol=1e-03, rtol=0)


# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>


# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
class test_multi_matrix_product():
    def test_consistency_multi_matrix_product(self):
        # Outputs type depending on intput type shall be :
        # IN :             
        # rot_mat :             [3,3]INT or FLOAT  | [3,3]INT or FLOAT  | [3,3,X]INT OR FLOAT | [3,3,X]
        # points_to_rotate :    [3]INT OR FLOAT    | [3,1] INT OR FLOAT | [3,X] INT OR FLOAT  | [3]
        # __________________________________________|____________________|_____________________|________
        # OUT :                                    |                    |             
        # result  :                  [3]INTor Fl   |   [3,1]INT or Fl   |     [3,X] int or FL |  [3,1]


        # case with 1D vectors and 2D matrix
        rot_mat = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        points_to_rotate = np.array([1, 2, 3])
        result = geo.multi_matrix_product(rot_mat, points_to_rotate)

        npt.assert_array_equal(result.ndim, 1)

        # case with 1D vector and 3D matrix
        rot_mat = np.transpose(np.array([[[1, 0, 0], [0, 1, 0], [0, 0, 1]]]), (1, 2, 0))
        points_to_rotate = np.array([1, 2, 3])
        result = geo.multi_matrix_product(rot_mat, points_to_rotate)

        npt.assert_array_equal(result.ndim, 2)

        # case with 2D vector and 2D matrix
        rot_mat = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        points_to_rotate = np.array([[1, 2, 3]]).T
        result = geo.multi_matrix_product(rot_mat, points_to_rotate)

        npt.assert_array_equal(result.ndim, 2)

        # case with 1D vector and 3D matrix
        rot_mat = np.transpose(np.array([[[1, 0, 0], [0, 1, 0], [0, 0, 1]]]), (1, 2, 0))
        points_to_rotate = np.array([[1, 2, 3]])
        result = geo.multi_matrix_product(rot_mat, points_to_rotate)

        npt.assert_array_equal(result.ndim, 2)

        # case with 2D vectors


# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>


# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
class sat_2_az_elev_test():
    # ------------------------------------------------------------------------
    def test_specific_values(self):
        # test over some hand-computed examples
        test_values = np.array([[0, 1, 1], \
                                [1, 0, 1], \
                                [1, 1, 1]]).T

        obtained_result = geo.compute_az_elev(test_values) * 180 / np.pi  # conversion into degrees

        expected_result = np.array([[0, 45.0], [45.0, 0], [45.0, 35.264389]]).T

        npt.assert_allclose(obtained_result, expected_result, atol=1e-03, rtol=0)


# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>


# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
class test_a_b_2_unitary_uvw():
    # ------------------------------------------------------------------------
    def test_specific_values2(self):
        # test over some hand-computed examples
        test_values = np.array([[0, 45.0], [45.0, 0], [45.0, 35.264389]]).T * np.pi / 180
        #        test_values = np.array([[45.0,0]]).T*np.pi/180

        obtained_result = geo.a_b_2_unitary_uvw(test_values)  # conversion into degrees

        expected_result = np.array([[0, 0.707106, 0.707106], \
                                    [0.707106, 0, 0.707106], \
                                    [0.5773502, 0.5773502, 0.5773502]]).T

        npt.assert_allclose(obtained_result, expected_result, atol=1e-03, rtol=0)


# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>




if __name__ == '__main__':
    #    npt.run_module_suite(argv = ['verbosity','2'])
    npt.run_module_suite()


    # expected_result[1,3]-obtained_result[1,3]
