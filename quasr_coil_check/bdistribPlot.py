#!/usr/bin/env python

import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy as np
from scipy.io import netcdf
from scipy.interpolate import interp1d
import math

import plotly.express as px


def main(fname):
    def maximizeWindow():
        # Maximize window. The command for this depends on the backend.
        mng = plt.get_current_fig_manager()
        try:
            mng.resize(*mng.window.maxsize())
        except AttributeError:
            try:
                mng.window.showMaximized()
            except AttributeError:
                pass

    f = netcdf.netcdf_file(fname, "r", mmap=False)
    nfp = f.variables["nfp"][()]
    nu_plasma = f.variables["nu_plasma"][()]
    nu_middle = f.variables["nu_middle"][()]
    nu_outer = f.variables["nu_outer"][()]
    nv_plasma = f.variables["nv_plasma"][()]
    nv_middle = f.variables["nv_middle"][()]
    nv_outer = f.variables["nv_outer"][()]
    nvl_plasma = f.variables["nvl_plasma"][()]
    nvl_middle = f.variables["nvl_middle"][()]
    nvl_outer = f.variables["nvl_outer"][()]
    u_plasma = f.variables["u_plasma"][()]
    u_middle = f.variables["u_middle"][()]
    u_outer = f.variables["u_outer"][()]
    v_plasma = f.variables["v_plasma"][()]
    v_middle = f.variables["v_middle"][()]
    v_outer = f.variables["v_outer"][()]
    vl_plasma = f.variables["vl_plasma"][()]
    vl_middle = f.variables["vl_middle"][()]
    vl_outer = f.variables["vl_outer"][()]
    r_plasma = f.variables["r_plasma"][()]
    r_middle = f.variables["r_middle"][()]
    r_outer = f.variables["r_outer"][()]
    xm_plasma = f.variables["xm_plasma"][()]
    xm_middle = f.variables["xm_middle"][()]
    xm_outer = f.variables["xm_outer"][()]
    xn_plasma = f.variables["xn_plasma"][()]
    xn_middle = f.variables["xn_middle"][()]
    xn_outer = f.variables["xn_outer"][()]
    mnmax_plasma = f.variables["mnmax_plasma"][()]
    mnmax_middle = f.variables["mnmax_middle"][()]
    mnmax_outer = f.variables["mnmax_outer"][()]
    svd_s_inductance_plasma_outer = f.variables["svd_s_inductance_plasma_outer"][()]
    svd_s_inductance_middle_outer = f.variables["svd_s_inductance_middle_outer"][()]
    svd_s_inductance_plasma_middle = f.variables["svd_s_inductance_plasma_middle"][()]
    svd_s_transferMatrix = f.variables["svd_s_transferMatrix"][()]
    svd_u_transferMatrix_uv = f.variables["svd_u_transferMatrix_uv"][()]
    svd_v_transferMatrix_uv = f.variables["svd_v_transferMatrix_uv"][()]
    svd_u_inductance_plasma_middle_uv = f.variables[
        "svd_u_inductance_plasma_middle_uv"
    ][()]
    svd_v_inductance_plasma_middle_uv = f.variables[
        "svd_v_inductance_plasma_middle_uv"
    ][()]
    n_pseudoinverse_thresholds = f.variables["n_pseudoinverse_thresholds"][()]
    n_singular_vectors_to_save = f.variables["n_singular_vectors_to_save"][()]
    pseudoinverse_thresholds = f.variables["pseudoinverse_thresholds"][()]
    check_orthogonality = False
    try:
        should_be_identity_plasma = f.variables["should_be_identity_plasma"][()]
        should_be_identity_middle = f.variables["should_be_identity_middle"][()]
        should_be_identity_outer = f.variables["should_be_identity_outer"][()]
        check_orthogonality = True
    except:
        pass

    try:
        overlap_plasma = f.variables["overlap_plasma"][()]
        overlap_middle = f.variables["overlap_middle"][()]
        overlap_exists = True
    except:
        overlap_exists = False

    try:
        Bnormal_from_1_over_R_field = f.variables["Bnormal_from_1_over_R_field"][()]
        Bnormal_from_1_over_R_field_uv = f.variables["Bnormal_from_1_over_R_field_uv"][
            ()
        ]
        Bnormal_from_1_over_R_field_inductance = f.variables[
            "Bnormal_from_1_over_R_field_inductance"
        ][()]
        Bnormal_from_1_over_R_field_transfer = f.variables[
            "Bnormal_from_1_over_R_field_transfer"
        ][()]
        one_over_R_exists = True
    except:
        one_over_R_exists = False

    try:
        Bnormal_from_const_v_coils = f.variables["Bnormal_from_const_v_coils"][()]
        Bnormal_from_const_v_coils_uv = f.variables["Bnormal_from_const_v_coils_uv"][()]
        Bnormal_from_const_v_coils_inductance = f.variables[
            "Bnormal_from_const_v_coils_inductance"
        ][()]
        Bnormal_from_const_v_coils_transfer = f.variables[
            "Bnormal_from_const_v_coils_transfer"
        ][()]
        const_v_exists = True
    except:
        const_v_exists = False

    try:
        Bnormal_from_plasma_current = f.variables["Bnormal_from_plasma_current"][()]
        Bnormal_from_plasma_current_uv = f.variables["Bnormal_from_plasma_current_uv"][
            ()
        ]
        Bnormal_from_plasma_current_inductance = f.variables[
            "Bnormal_from_plasma_current_inductance"
        ][()]
        Bnormal_from_plasma_current_transfer = f.variables[
            "Bnormal_from_plasma_current_transfer"
        ][()]
        plasma_current_exists = True
    except:
        plasma_current_exists = False

    print("nu_plasma: ", nu_plasma)
    print("nvl_plasma: ", nvl_plasma)
    print("r_plasma.shape: ", r_plasma.shape)
    print("svd_s_transferMatrix.shape: ", svd_s_transferMatrix.shape)
    print("svd_u_transferMatrix_uv.shape: ", svd_u_transferMatrix_uv.shape)

    f.close()

    ########################################################
    # Plot singular values
    ########################################################

    figureNum = 1
    fig = plt.figure(figureNum)
    fig.patch.set_facecolor("white")

    plt.plot(
        svd_s_inductance_middle_outer,
        ".m",
        label="Inductance matrix between middle and outer surfaces",
    )
    plt.plot(
        svd_s_inductance_plasma_outer,
        ".r",
        label="Inductance matrix between plasma and outer surfaces",
    )
    plt.plot(
        svd_s_inductance_plasma_middle,
        ".g",
        label="Inductance matrix between plasma and middle surfaces",
    )
    # plt.plot(svd_s_inductance_plasma_middle,'.g',label='Inductance matrix between plasma and control surfaces')
    colors = [
        "k",
        "orange",
        "c",
        "brown",
        "gray",
        "darkred",
        "olive",
        "darkviolet",
        "gold",
        "lawngreen",
    ]
    for i in range(n_pseudoinverse_thresholds):
        plt.plot(
            svd_s_transferMatrix[i, :], ".", color=colors[i], label="Transfer matrix"
        )
    #    plt.plot(svd_s_transferMatrix[i,:],'.',color=colors[i],label='Transfer matrix, thresh='+str(pseudoinverse_thresholds[i]))
    plt.legend(fontsize="x-small", loc=3)
    plt.title("Singular values")
    plt.yscale("log")

    ########################################################
    # check_orthogonality plot
    ########################################################

    if check_orthogonality:
        figureNum += 1
        fig = plt.figure(figureNum)
        fig.patch.set_facecolor("white")

        numRows = 1
        numCols = 3
        th = 1e-17

        plt.subplot(numRows, numCols, 1)
        data = np.abs(should_be_identity_plasma.transpose())
        data[data < th] = th
        plt.pcolormesh(np.log10(data))
        plt.gca().invert_yaxis()
        plt.colorbar()
        plt.title("should_be_identity_plasma")

        plt.subplot(numRows, numCols, 2)
        data = np.abs(should_be_identity_middle.transpose())
        data[data < th] = th
        plt.pcolormesh(np.log10(data))
        plt.gca().invert_yaxis()
        plt.colorbar()
        plt.title("should_be_identity_middle")

        plt.subplot(numRows, numCols, 3)
        data = np.abs(should_be_identity_outer.transpose())
        data[data < th] = th
        plt.pcolormesh(np.log10(data))
        plt.gca().invert_yaxis()
        plt.colorbar()
        plt.title("should_be_identity_outer")

        maximizeWindow()

        figureNum += 1
        fig = plt.figure(figureNum)
        fig.patch.set_facecolor("white")

        numRows = 1
        numCols = 1
        th = 1e-17

        data = np.abs(np.diag(should_be_identity_plasma) - 1)
        data[data < th] = th
        plt.plot(np.log10(data), label="plasma")

        data = np.abs(np.diag(should_be_identity_middle) - 1)
        data[data < th] = th
        plt.plot(np.log10(data), label="middle")

        data = np.abs(np.diag(should_be_identity_outer) - 1)
        data[data < th] = th
        plt.plot(np.log10(data), label="outer")

        plt.title("log10(diag(should_be_identity)-1)    This should be very small.")
        plt.legend()

        maximizeWindow()

    ########################################################
    # For 3D plotting, 'close' the arrays in u and v
    ########################################################

    r_plasma = np.append(r_plasma, r_plasma[[0], :, :], axis=0)
    r_plasma = np.append(r_plasma, r_plasma[:, [0], :], axis=1)
    vl_plasma = np.append(vl_plasma, nfp)

    r_middle = np.append(r_middle, r_middle[[0], :, :], axis=0)
    r_middle = np.append(r_middle, r_middle[:, [0], :], axis=1)
    vl_middle = np.append(vl_middle, nfp)

    r_outer = np.append(r_outer, r_outer[[0], :, :], axis=0)
    r_outer = np.append(r_outer, r_outer[:, [0], :], axis=1)
    vl_outer = np.append(vl_outer, nfp)

    ########################################################
    # Extract cross-sections of the 3 surfaces at several toroidal angles
    ########################################################

    def getCrossSection(rArray, vl_old, v_new):
        vl_old = np.concatenate((vl_old - nfp, vl_old))
        rArray = np.concatenate((rArray, rArray), axis=0)

        print("vl_old shape:", vl_old.shape)
        print("rArray shape:", rArray.shape)

        x = rArray[:, :, 0]
        y = rArray[:, :, 1]
        z = rArray[:, :, 2]
        R = np.sqrt(x**2 + y**2)

        nu = z.shape[1]
        nv_new = len(v_new)
        R_slice = np.zeros([nv_new, nu])
        Z_slice = np.zeros([nv_new, nu])
        for iu in range(nu):
            interpolator = interp1d(vl_old, R[:, iu])
            R_slice[:, iu] = interpolator(v_new)
            interpolator = interp1d(vl_old, z[:, iu])
            Z_slice[:, iu] = interpolator(v_new)

        return R_slice, Z_slice

    v_slices = [0, 0.25, 0.5, 0.75]

    # import plotly.graph_objects as go

    # fig = go.Figure()

    # # Add the first surface (r_plasma)
    # fig.add_trace(
    #     go.Surface(
    #         z=r_plasma[:, :, 2],
    #         x=r_plasma[:, :, 0],
    #         y=r_plasma[:, :, 1],
    #         colorscale="Viridis",
    #         name="r_plasma",
    #     )
    # )
    # fig.show()
    # fig = go.Figure()

    # # Add the second surface (r_middle)
    # fig.add_trace(
    #     go.Surface(
    #         z=r_middle[:, :, 2],
    #         x=r_middle[:, :, 0],
    #         y=r_middle[:, :, 1],
    #         colorscale="Cividis",
    #         name="r_middle",
    #         showscale=False,
    #     )
    # )
    # fig.show()
    # fig = go.Figure()

    # # Add the third surface (r_outer)
    # fig.add_trace(
    #     go.Surface(
    #         z=r_outer[:, :, 2],
    #         x=r_outer[:, :, 0],
    #         y=r_outer[:, :, 1],
    #         colorscale="Plasma",
    #         name="r_outer",
    #         showscale=False,
    #     )
    # )
    # fig.show()
    R_slice_plasma, Z_slice_plasma = getCrossSection(r_plasma, vl_plasma, v_slices)
    R_slice_middle, Z_slice_middle = getCrossSection(r_middle, vl_middle, v_slices)
    R_slice_outer, Z_slice_outer = getCrossSection(r_outer, vl_outer, v_slices)

    ########################################################
    # Now make plot of surfaces at given toroidal angle
    ########################################################

    figureNum += 1
    fig = plt.figure(figureNum)
    fig.patch.set_facecolor("white")

    numRows = 2
    numCols = 2

    Rmin = R_slice_outer.min()
    Rmax = R_slice_outer.max()
    Zmin = Z_slice_outer.min()
    Zmax = Z_slice_outer.max()

    for whichPlot in range(4):
        plt.subplot(numRows, numCols, whichPlot + 1)
        v = v_slices[whichPlot]
        plt.plot(
            R_slice_outer[whichPlot, :],
            Z_slice_outer[whichPlot, :],
            "b.-",
            label="outer",
        )
        plt.plot(
            R_slice_middle[whichPlot, :],
            Z_slice_middle[whichPlot, :],
            "m.-",
            label="control",
        )
        plt.plot(
            R_slice_plasma[whichPlot, :],
            Z_slice_plasma[whichPlot, :],
            "r.-",
            label="plasma",
        )
        plt.gca().set_aspect("equal", adjustable="box")
        plt.legend(fontsize="x-small")
        plt.title("v=" + str(v))
        plt.xlabel("R")
        plt.ylabel("Z")
        plt.xlim([Rmin, Rmax])
        plt.ylim([Zmin, Zmax])

    plt.tight_layout()

    ########################################################
    # Prepare for plotting singular vectors
    ########################################################

    maxVectorsToPlot = 25
    numVectorsToPlot = min(maxVectorsToPlot, n_singular_vectors_to_save)
    # If more vectors are saved than the number allowed to plot, then plot the last ones saved.
    # plotOffset = n_singular_vectors_to_save - numVectorsToPlot
    plotOffset = 0
    mpl.rc("xtick", labelsize=7)
    mpl.rc("ytick", labelsize=7)
    numCols = int(np.ceil(np.sqrt(numVectorsToPlot)))
    numRows = int(np.ceil(numVectorsToPlot * 1.0 / numCols))

    numContours = 20

    ########################################################
    # Plot singular vectors of the plasma-middle inductance matrix on the plasma surface
    ########################################################

    figureNum += 1
    fig = plt.figure(figureNum)
    fig.patch.set_facecolor("white")

    for whichPlot in range(numVectorsToPlot):
        plt.subplot(numRows, numCols, whichPlot + 1)
        data = np.reshape(
            svd_u_inductance_plasma_middle_uv[whichPlot + plotOffset, :],
            [nu_plasma, nv_plasma],
            order="F",
        )
        plt.contourf(v_plasma, u_plasma, data, numContours)
        # plt.colorbar()
        plt.xlabel("v", fontsize="x-small")
        plt.ylabel("u", fontsize="x-small")
        plt.title(
            "Singular vector U "
            + str(whichPlot + plotOffset + 1)
            + "\ns="
            + str(svd_s_inductance_plasma_middle[whichPlot + plotOffset]),
            fontsize="x-small",
        )

        plt.tight_layout()
        ax = fig.add_axes((0, 0, 1, 1), frameon=False)
        ax.text(
            0.5,
            0.99,
            "Singular vectors of the plasma-to-middle surface inductance matrix. (U vectors = plasma surface)",
            horizontalalignment="center",
            verticalalignment="top",
            fontsize="small",
        )

    ########################################################
    # Plot singular vectors of the plasma-middle inductance matrix on the middle surface
    ########################################################

    figureNum += 1
    fig = plt.figure(figureNum)
    fig.patch.set_facecolor("white")

    for whichPlot in range(numVectorsToPlot):
        plt.subplot(numRows, numCols, whichPlot + 1)
        data = np.reshape(
            svd_v_inductance_plasma_middle_uv[whichPlot + plotOffset, :],
            [nu_middle, nv_middle],
            order="F",
        )
        plt.contourf(v_middle, u_middle, data, numContours)
        # plt.colorbar()
        plt.xlabel("v", fontsize="x-small")
        plt.ylabel("u", fontsize="x-small")
        plt.title(
            "Singular vector V "
            + str(whichPlot + plotOffset + 1)
            + "\ns="
            + str(svd_s_inductance_plasma_middle[whichPlot + plotOffset]),
            fontsize="x-small",
        )

        plt.tight_layout()
        ax = fig.add_axes((0, 0, 1, 1), frameon=False)
        ax.text(
            0.5,
            0.99,
            "Singular vectors of the plasma-to-middle surface inductance matrix. (V vectors = middle surface)",
            horizontalalignment="center",
            verticalalignment="top",
            fontsize="small",
        )

    ########################################################
    # Plot singular vectors of the transfer matrix on the plasma surface
    ########################################################

    for whichThreshold in range(n_pseudoinverse_thresholds):
        figureNum += 1
        fig = plt.figure(figureNum)
        fig.patch.set_facecolor("white")

        for whichPlot in range(numVectorsToPlot):
            plt.subplot(numRows, numCols, whichPlot + 1)
            data = np.reshape(
                svd_u_transferMatrix_uv[whichThreshold, whichPlot + plotOffset, :],
                [nu_plasma, nv_plasma],
                order="F",
            )
            plt.contourf(v_plasma, u_plasma, data, numContours)
            # plt.colorbar()
            plt.xlabel("v", fontsize="x-small")
            plt.ylabel("u", fontsize="x-small")
            plt.title(
                "Singular vector U "
                + str(whichPlot + plotOffset + 1)
                + "\ns="
                + str(svd_s_transferMatrix[whichThreshold, whichPlot + plotOffset]),
                fontsize="x-small",
            )

        plt.tight_layout()
        ax = fig.add_axes((0, 0, 1, 1), frameon=False)
        ax.text(
            0.5,
            0.99,
            "Singular vectors of the transfer matrix. U vectors = plasma surface. (threshold="
            + str(pseudoinverse_thresholds[whichThreshold])
            + ")",
            horizontalalignment="center",
            verticalalignment="top",
            fontsize="small",
        )

    ########################################################
    # Plot singular vectors of the transfer matrix on the middle surface
    ########################################################

    for whichThreshold in range(n_pseudoinverse_thresholds):
        figureNum += 1
        fig = plt.figure(figureNum)
        fig.patch.set_facecolor("white")

        for whichPlot in range(numVectorsToPlot):
            plt.subplot(numRows, numCols, whichPlot + 1)
            data = np.reshape(
                svd_v_transferMatrix_uv[whichThreshold, whichPlot + plotOffset, :],
                [nu_middle, nv_middle],
                order="F",
            )
            plt.contourf(v_middle, u_middle, data, numContours)
            # plt.colorbar()
            plt.xlabel("v", fontsize="x-small")
            plt.ylabel("u", fontsize="x-small")
            plt.title(
                "Singular vector V "
                + str(whichPlot + plotOffset + 1)
                + "\ns="
                + str(svd_s_transferMatrix[whichThreshold, whichPlot + plotOffset]),
                fontsize="x-small",
            )

        plt.tight_layout()
        ax = fig.add_axes((0, 0, 1, 1), frameon=False)
        ax.text(
            0.5,
            0.99,
            "Singular vectors of the transfer matrix. V vectors = middle surface. (threshold="
            + str(pseudoinverse_thresholds[whichThreshold])
            + ")",
            horizontalalignment="center",
            verticalalignment="top",
            fontsize="small",
        )

    ########################################################
    # Now make 3D surface plot
    ########################################################

    # figureNum += 1
    # fig = plt.figure(figureNum)
    # fig.patch.set_facecolor('white')
    # ax = fig.gca(projection='3d')
    # ax.plot_surface(r_plasma[:,:,0], r_plasma[:,:,1], r_plasma[:,:,2], rstride=1, cstride=1, color='r',linewidth=0)
    #
    # maxIndex = int(nvl_middle*0.7)
    # ax.plot_surface(r_middle[:maxIndex,:,0], r_middle[:maxIndex,:,1], r_middle[:maxIndex,:,2], rstride=1, cstride=1, color='m',linewidth=0)
    #
    # maxIndex = int(nvl_outer*0.55)
    # minIndex = int(nvl_outer*0.15)
    # ax.plot_surface(r_outer[minIndex:maxIndex,:,0], r_outer[minIndex:maxIndex,:,1], r_outer[minIndex:maxIndex,:,2], rstride=1, cstride=1, color='b',linewidth=0)
    #
    # plotLMax = r_outer.max()
    # ax.auto_scale_xyz([-plotLMax, plotLMax], [-plotLMax, plotLMax], [-plotLMax, plotLMax])

    ########################################################
    # Plot overlap of transfer matrix and inductance matrix singular vectors
    ########################################################

    if overlap_exists:
        # execfile('/global/homes/l/landrema/scripts/colormaps.py')
        ##myCmap=viridis
        # myCmap=plasma
        # myCmap = inferno
        myCmap = "inferno"

        figureNum += 1
        fig = plt.figure(figureNum)
        fig.patch.set_facecolor("white")

        numRows = 1
        numCols = 2
        my_clim = (-4.0, 0.0)

        plt.subplot(numRows, numCols, 1)
        # plt.imshow(np.log10(np.abs(overlap_plasma)),interpolation='none',clim=my_clim)
        # plt.imshow(np.log10(np.abs(overlap_plasma.transpose())),interpolation='none',clim=my_clim,cmap=myCmap)
        plt.imshow(
            np.log10(np.abs(overlap_plasma.transpose())),
            interpolation="none",
            clim=my_clim,
        )
        # plt.gca().xaxis.tick_top()
        plt.colorbar()
        plt.title(
            "Log10 overlap of transfer and inductance singular vectors on plasma surface"
        )
        plt.xlabel("Index of inductance singular vector")
        plt.ylabel("Index of transfer singular vector")

        plt.subplot(numRows, numCols, 2)
        # plt.imshow(np.log10(np.abs(overlap_middle)),interpolation='none',clim=my_clim)
        # plt.imshow(np.log10(np.abs(overlap_middle.transpose())),interpolation='none',clim=my_clim,cmap=myCmap)
        plt.imshow(
            np.log10(np.abs(overlap_middle.transpose())),
            interpolation="none",
            clim=my_clim,
        )
        # plt.gca().xaxis.tick_top()
        plt.colorbar()
        plt.title(
            "Log10 overlap of transfer and inductance singular vectors on middle surface"
        )
        plt.xlabel("Index of inductance singular vector")
        plt.ylabel("Index of transfer singular vector")

        maximizeWindow()

    #######################################################
    # Plot quantities related to 1/R field
    ########################################################

    if one_over_R_exists or const_v_exists or plasma_current_exists:

        figureNum += 1
        fig = plt.figure(figureNum)
        fig.patch.set_facecolor("white")

        numRows = 2
        numCols = 3
        titleFontSize = 10

        if one_over_R_exists:
            plt.subplot(numRows, numCols, 1)
            plt.contourf(
                v_plasma,
                u_plasma,
                Bnormal_from_1_over_R_field_uv.transpose(),
                numContours,
            )
            plt.xlabel("v", fontsize="x-small")
            plt.ylabel("u", fontsize="x-small")
            # plt.imshow(,interpolation='none')
            ##plt.gca().xaxis.tick_top()
            plt.colorbar()
            plt.title("1/R toroidal field\n(component normal to plasma surface)")
            # plt.xlabel('iu')
            # plt.ylabel('iv')

            plt.subplot(numRows, numCols, 4)
            plt.semilogy(
                abs(Bnormal_from_1_over_R_field), "x-", label="Basis functions"
            )
            plt.semilogy(
                abs(Bnormal_from_1_over_R_field_inductance),
                "x-",
                label="Left-singular vectors of inductance matrix",
            )
            plt.semilogy(
                abs(Bnormal_from_1_over_R_field_transfer),
                "x-",
                label="Left-singular vectors of transfer matrix",
            )
            plt.title(
                "abs (Bnormal_from_1_over_R_field) on the plasma surface",
                fontsize=titleFontSize,
            )
            plt.xlabel("index")
            plt.legend(fontsize=8)

        if const_v_exists:
            plt.subplot(numRows, numCols, 2)
            plt.contourf(
                v_plasma,
                u_plasma,
                Bnormal_from_const_v_coils_uv.transpose(),
                numContours,
            )
            plt.xlabel("v", fontsize="x-small")
            plt.ylabel("u", fontsize="x-small")
            # plt.imshow(,interpolation='none')
            ##plt.gca().xaxis.tick_top()
            plt.colorbar()
            plt.title(
                "B field due to constant-v coils\n(component normal to plasma surface)"
            )
            # plt.xlabel('iu')
            # plt.ylabel('iv')

            plt.subplot(numRows, numCols, 5)
            plt.semilogy(abs(Bnormal_from_const_v_coils), "+-", label="Basis functions")
            plt.semilogy(
                abs(Bnormal_from_const_v_coils_inductance),
                "+-",
                label="Left-singular vectors of inductance matrix",
            )
            plt.semilogy(
                abs(Bnormal_from_const_v_coils_transfer),
                "+-",
                label="Left-singular vectors of transfer matrix",
            )
            plt.title(
                "abs (Bnormal_from_const_v_coils) on the plasma surface",
                fontsize=titleFontSize,
            )
            plt.xlabel("index")
            plt.legend(fontsize=8)

        if plasma_current_exists:
            plt.subplot(numRows, numCols, 3)
            plt.contourf(
                v_plasma,
                u_plasma,
                Bnormal_from_plasma_current_uv.transpose(),
                numContours,
            )
            plt.xlabel("v", fontsize="x-small")
            plt.ylabel("u", fontsize="x-small")
            # plt.imshow(,interpolation='none')
            ##plt.gca().xaxis.tick_top()
            plt.colorbar()
            plt.title(
                "B field due to plasma current\n(component normal to plasma surface)"
            )
            # plt.xlabel('iu')
            # plt.ylabel('iv')

            plt.subplot(numRows, numCols, 6)
            try:
                plt.semilogy(
                    abs(Bnormal_from_plasma_current), "+-", label="Basis functions"
                )
                plt.semilogy(
                    abs(Bnormal_from_plasma_current_inductance),
                    "+-",
                    label="Left-singular vectors of inductance matrix",
                )
                plt.semilogy(
                    abs(Bnormal_from_plasma_current_transfer),
                    "+-",
                    label="Left-singular vectors of transfer matrix",
                )
            except:
                # May give an error if values are all 0
                pass

            plt.title(
                "abs (Bnormal_from_plasma_current) on the plasma surface",
                fontsize=titleFontSize,
            )
            plt.xlabel("index")
            plt.legend(fontsize=8)

        maximizeWindow()

    plt.show()


if __name__ == "__main__":

    print("usage: python bdistribPlot.py bdistrib_out.XXX.nc")

    import sys

    if len(sys.argv) != 2:
        print("Error! You must specify 1 argument: the bdistrib_out.XXX.nc file.")
        exit(1)
    main(sys.argv[1])
