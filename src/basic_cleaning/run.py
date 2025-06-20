#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging

import pandas as pd
import wandb

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################
    local_path = wandb.use_artifact(args.input_artifact).file()
    logger.info(f"{args.input_artifact} is downloaded")

    df = pd.read_csv(local_path)

    idx = df["price"].between(args.min_price, args.max_price)
    df = df[idx].copy()
    logger.info(
        f"Only prices between {args.min_price} and {args.max_price} are taken into consideration."
    )

    df["last_review"] = pd.to_datetime(df["last_review"])

    idx = df["longitude"].between(-74.25, -73.50) & df["latitude"].between(40.5, 41.2)
    df = df[idx].copy()
    df.to_csv(args.output_artifact, index=False)
    logger.info(f"{args.output_artifact} saved.")

    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file(args.output_artifact)
    run.log_artifact(artifact)
    logger.info(f"{args.output_artifact} uploaded to Weights and Biases.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")

    parser.add_argument(
        "--input_artifact", type=str, help="Name of input artifact", required=True
    )

    parser.add_argument(
        "--output_artifact", type=str, help="Name of output artifact", required=True
    )

    parser.add_argument(
        "--output_type", type=str, help="Type for output artifact", required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="Description for output artifact",
        required=True,
    )

    parser.add_argument(
        "--min_price", type=float, help="Minimal price to consider", required=True
    )

    parser.add_argument(
        "--max_price", type=float, help="Maximal price to consider", required=True
    )

    args = parser.parse_args()

    go(args)
